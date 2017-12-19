#-*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
import itertools
import argparse
import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.coders import coders

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class JsonExtractEvent(beam.DoFn):
    def __init__(self):
        super(JsonExtractEvent, self).__init__()

    def process(self, json_file):
        json_file = json.loads(json_file) #direct runner일 경우만 on, bigquery는 off
        print 'signal ', json_file

        # this part is for bigquery
        user_id = json_file['user_id'] if json_file['user_id'] is not None else ' '
        instance_id = json_file['app_instance_id']
        app_platform = json_file['app_platform'] if json_file['app_platform'] is not None else ' '
        country = json_file['country'] if json_file['country'] is not None else ' '

        date = json_file['date']
        event = json_file['name']
        pair = "\t".join([user_id, instance_id, date, app_platform, country, event])

        yield pair


class CountUser(beam.PTransform):
    def __init__(self):
        pass

    def expand(self, pcoll):
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
    pipeline_options.view_as(SetupOptions).save_main_session = False


    p = beam.Pipeline(options=pipeline_options)
    query = "SELECT user_dim.user_id, user_dim.app_info.app_instance_id, user_dim.app_info.app_platform, " \
            "user_dim.app_info.app_version, user_dim.geo_info.country, event.* " \
            "FROM `table`, UNNEST(event_dim) as event "

    lines = p | 'read' >> beam.io.Read(beam.io.BigQuerySource(
                query=query, use_standard_sql=True))

    counts = (lines
              | 'data_extract' >> (beam.ParDo(JsonExtractEvent())).with_output_types(unicode)
              )

    counts | 'write' >> WriteToText(known_args.output, coder=coders.ToStringCoder(), num_shards=1)


    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()