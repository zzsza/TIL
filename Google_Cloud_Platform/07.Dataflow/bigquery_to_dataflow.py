#-*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
import argparse
import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.coders import coders
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# ToDo : DAU, WAU, MAU, Retention
# ToDo : User Count
# ToDo : 시간차 맞추기 ( 클라이언트와 서버 ) -> 이건 양립할 순 없는 것 같고 파라미터를 쓴다면 클라가 좋음
# ToDo : \t로 사용할지 결정하기, 빈칸일 경우 어떻게 처리할지? (done)
# ToDo : 특정 이벤트는 전처리 단계 초반에서 pass하기 (user_engagement 같은 것들)
# ToDo : BigQuery에서 IO를 더 줄이면서 데이터 가져오는 방법 찾아보기 (계속 ing)
# ToDo : 클래스화 해서 합치기


class JsonExtractEvent(beam.DoFn):
    def __init__(self):
        super(JsonExtractEvent, self).__init__()

    def process(self, json_file):
        def parameter_extract(parameter_json):
            # ToDo : parameter가 firebase_screen_class, firebase_conversion, firebase_screen_id면 pass하도록 여기에 추가
            if isinstance(parameter_json, unicode):
                temp_list.append(parameter_json)
            elif isinstance(parameter_json, dict):
                if parameter_json['string_value'] is not None:
                    temp_list.append(parameter_json['string_value'])
                elif parameter_json['int_value'] is not None:
                    temp_list.append(str(parameter_json['int_value']))
                else:
                    temp_list.append(str(parameter_json['double_value']))
            else:
                pass
            return temp_list

        # json_file = json.loads(json_file)  # direct runner일 경우만 on, bigquery는 off

        # this part is for bigquery
        user_id = json_file['user_id'] if json_file['user_id'] is not None else ' ' if not json_file['user_id'] else ' '
        instance_id = json_file['app_instance_id'] if json_file['app_instance_id'] is not None else ' ' if not json_file['app_instance_id'] else ' '
        app_platform = json_file['app_platform'] if json_file['app_platform'] is not None else ' ' if not json_file['app_platform'] else ' '
        country = json_file['country'] if json_file['country'] is not None else ' ' if not json_file['country'] else ' '

        date = json_file['date']
        timestamp = str(json_file['timestamp_micros'])
        event = json_file['name']

        platform = 'client'

        if platform == 'client':
            value_list = []
            for i, v in enumerate(json_file['params']):
                temp_list = []
                for j, h in v.items():
                    extract_list = parameter_extract(h)
                parameter_value = "0x16".join(extract_list)  # key, value split 단위
                value_list.append(parameter_value)

            value_string = '0x10'.join(value_list)
        else:
            value_string = ''

        pair = "\t".join([event, date, country, app_platform, instance_id, timestamp, value_string])
        yield pair


class CountUser(beam.PTransform):
    def __init__(self):
        pass

    def expand(self, pcoll):
        return (pcoll
                | beam.combiners.Count.PerKey()
                )


def count_total(word_ones):
    print('word_ones :', word_ones)
    (word, ones) = word_ones
    return [x.encode('utf-8') for x in word], sum(ones)


def run(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--input',
                        dest='input',
                        default='gs://dev-temp/tmp/test2.json',
                        help='Input file')

    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        default='gs://dev-temp/tmp/dataflow/',
                        help='Output file to write result')

    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = False


    p = beam.Pipeline(options=pipeline_options)
    client_query = "SELECT user_dim.user_id, user_dim.app_info.app_instance_id, user_dim.app_info.app_platform, " \
            "user_dim.app_info.app_version, user_dim.geo_info.country, event.* " \
            "FROM `com_bootstlab_retro_IOS.app_events_20180101`, UNNEST(event_dim) as event limit 1000"
    server_query = "SELECT user_id, device_id, event_name as name, CAST(timestamp_nanos/1000 AS INT64) as timestamp_micros, MAX(IF(event_params.key = 'StatusCode', event_params.value.string_value, null)) as status_code " \
            "FROM `server_logs_us.events_20180102`, UNNEST(event_params) AS event_params GROUP BY 1,2,3,4 HAVING statue_code = '200' limit 100 "

    lines = p | 'read_ios' >> beam.io.Read(beam.io.BigQuerySource(
                query=client_query, use_standard_sql=True, flatten_results=False))

    counts = (lines
              | 'data_extract' >> (beam.ParDo(JsonExtractEvent())).with_output_types(unicode)
              | 'pair_with_one' >> beam.Map(lambda x: (str(x.split('\t')[:4]), 1))  # [:4] : event, [1] : dau
              # | 'group_by_key' >> beam.GroupByKey()  # group by key를 하려면 위에서 tuple이 나와야 함
              | 'count_per_key' >> beam.combiners.Count.PerKey()
              # | 'count_user' >> beam.FlatMap(lambda x: len(x))
              # | 'count_total' >> beam.Map(count_total)
              )

    counts | 'write' >> WriteToText(known_args.output, coder=coders.ToStringCoder(), num_shards=1)

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()