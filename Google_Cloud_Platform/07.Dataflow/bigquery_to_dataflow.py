#-*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging

import argparse
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.io.gcp import bigquery
from apache_beam.coders import coders

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions



class JsonExtractEvent(beam.DoFn):
    def __init__(self):
        super(JsonExtractEvent, self).__init__()

    def process(self, json_file):
        user_id = json_file['user_dim']['app_info']['app_instance_id']
        event_name = json_file['event_dim'][0]['name']
        date = json_file['event_dim'][0]['date']
        pair = "\t".join([user_id, event_name, date])
        # 여기의 print는 콘솔에 출력이 안되지만 스택드라이버에 다 로그가 남음!
        # unicode로 될 경우에 에러 발생 -> [] 넣어야 함
        return [pair]

class CountUser(beam.PTransform):
    def __init__(self):
        pass

    def expand(self, pcoll):
        print('Count User Part', pcoll)
        return (pcoll
                | beam.combiners.Count.PerKey()
                )

def run(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--input',
                        dest='input',
                        default='gs://url',
                        help='Input file')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        default='gs://url',
                        help='Output file to write result')

    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True


    p = beam.Pipeline(options=pipeline_options)
    lines = p | 'read' >> beam.io.Read(beam.io.BigQuerySource(
                project='bigquery_project', dataset='temp', table='temp3', flatten_results=True))

    def count_total(word_ones):
        (word, ones) = word_ones
        return (word, sum(ones))

    counts = (lines
              | 'data_extract' >> (beam.ParDo(JsonExtractEvent())).with_output_types(unicode)
              | 'pair_with_one' >> beam.Map(lambda x: (x.split('\t')[1:], 1))
              | 'group' >> beam.GroupByKey()
              | 'count_total' >> beam.Map(count_total))

    # ToDo : 여기에서 count_ones가 아니라 max_ones를 취한 후 output에서 map을 취하면 User도 추출 가능 -> Count 메소드를 사용
    # ToDo : 파이프라인을 함수화해서 필요한 것만 사용하면 좋지 않을까?
    # ToDo : 병렬로 동시에 User, Total 구해서 한 row로 나오도록 만들기
    # ToDo : OrderBy해서 내림차순 - bash 혹은 bi tool에서 : pass
    # ToDo : 마지막에 유니코드를 string으로 변경해야할까? python2라 고민.. -> StringCoder를 사용하면 되는데 리스트 안에 있는 친구들은 안됨


    def format_result(word_count):
        (word, count) = word_count
        return '%s: %s' % (word, count)

    output = counts | 'format' >> beam.Map(format_result)

    output | 'write' >> WriteToText(known_args.output, coder=coders.ToStringCoder(), num_shards=1)
    # ToStringCoder 옵션을 주면 unicode가 string으로 변환되서 저장됨. list안에 있는 unicode는 변환이 안됨

    print('run')
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()