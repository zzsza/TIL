#-*- coding: utf-8 -*-

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# create pipeline
p = beam.Pipeline(options=PipelineOptions())

# configuring pipeline options
# option : runner, project id, location of storing file
# option : --<option>=<value>

# another custom option setting
class MyOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(clscls, parser):
        parser.add_argument('--input',
                            help='Input for the pipeline',
                            default='gs://my-bucket/input')
        parser.add_argument('--output',
                            help='Output for the pipeline',
                            default='gs://my-bucket/output')



# PCollection : pipeline data
# PCollection objects : inputs, outputs

# read from an external source
lines = p | "ReadFile" >> beam.io.ReadFromText('gs://dev-temp/tmp/dataflow.json')

# read from in-memory data(list)
with beam.Pipeline(options=MyOptions) as p:
  lines = (p
           | beam.Create([
               'To be, or not to be: that is the question: ',
               'Whether \'tis nobler in the mind to suffer ',
               'The slings and arrows of outrageous fortune, ',
               'Or to take arms against a sea of troubles, ']))


# PCollection 특징
# 특정 pipeline에 소유됨

# 1. 요소 유형 : 모든 유형이 가능하지만 모두 동일한 유형이어야 함.
# 분산 처리를 지원라혀려면 beam이 각 개별 요소를 바이트 문자열로 인코딩 할 수 있어야 함
# 2. 불변성 : PColeection은 변경 불가능 ( 이건 스파크에서 RDD의 개념처럼 변경 불가 )
# 일단 생성되면 개별 요소를 추가 제거 또는 변경할 수 없음
# 3. 무작위 액세스 : PCollection은 개별 요소에 대한 무작위 액세스를 지원하지 않음
# 대신 Beam Transform은 모든 요소를 개별적으로 고려
# 4. 크기와 경계 : PCollection에 포함할 수 있는 요소 상한이 없음
# 5. 각 요소들은 timestamp를 가지고 있음. 수동 할당도 가


# Transforms
# 파이프라인의 연산
# ParDo, Combine 등
# | : pipe operator로 apply method


# [Output PCollection] = [Input PCollection] | [Transform]
# [Final Output PCollection] = ([Initial Input PCollection] | [First Transform]
#               | [Second Transform]
#               | [Third Transform])

# [Output PCollection 1] = [Input PCollection] | [Transform 1]
# [Output PCollection 2] = [Input PCollection] | [Transform 2]


# Core Beam Transforms
# ParDo
# - general parallel processing을 위한 연산이며 Map과 유사함
# 다음과 같은 상황에 유용
# Filtering a data set
# Formatting 또는 type 변환 : 다른 타입을 가지고 있을 경우 변환
# 데이터셋의  특정 요소만 추출할 경우
# 데이터셋의 각 요소에 연산 수
# ParDo 변환을 적용할 때 DoFn 객체의 형태로 코드를 제공해야 함 (분산 처리 함수를 정의하는 클래스 )


words = 'hello dataflow'

class ComputeWordLengthFn(beam.DoFn):
    def process(selfself, element):
        return [len(element)]

word_lengths = words | beam.Pardo(ComputeWordLengthFn)


# lambda로도 표현 가능. FlatMap은 각각의 요소에 적용되는 Map
word_lengths = words | beam.FlatMap(lambda word: [len(word)])

# highlevel API Map 도 사용 가. Map은 1개의 출력을 할 경우 사용
word_lengths = words | beam.Map(len)


# GroupByKey
# key/value pairs 관련 연산
# aggregate할 경우 좋은 방법
# GroupByKey 또는 CoGroupByKey는 모든 key가 수집될때까지 기다림
# unbound(끝이 없는 경우로 stream) collection은 제한이 없음.
# 이 경우엔 non global windowinf을 사용하거나 aggregation trigger 사용

# CoGroupByKey
# 2개 이상의 ke value일 경우 사용

emails_list = [
    ('amy', 'amy@example.com'),
    ('carl', 'carl@example.com'),
    ('julia', 'julia@example.com'),
    ('carl', 'carl@email.com'),
]
phones_list = [
    ('amy', '111-222-3333'),
    ('james', '222-333-4444'),
    ('amy', '333-444-5555'),
    ('carl', '444-555-6666'),
]

emails = p | 'CreateEmails' >> beam.Create(emails_list)
phones = p | 'CreatePhones' >> beam.Create(phones_list)

# results = [
#     ('amy', {
#         'emails': ['amy@example.com'],
#         'phones': ['111-222-3333', '333-444-5555']}),
#     ('carl', {
#         'emails': ['carl@email.com', 'carl@example.com'],
#         'phones': ['444-555-6666']}),
#     ('james', {
#         'emails': [],
#         'phones': ['222-333-4444']}),
#     ('julia', {
#         'emails': ['julia@example.com'],
#         'phones': []}),
# ]

results = ({'emails': emails, 'phones': phones}
           | beam.CoGroupByKey())

def join_info(name_info):
  (name, info) = name_info
  return '%s; %s; %s' %\
      (name, sorted(info['emails']), sorted(info['phones']))

contact_lines = results | beam.Map(join_info)

# formatted_results = [
#     "amy; ['amy@example.com']; ['111-222-3333', '333-444-5555']",
#     "carl; ['carl@email.com', 'carl@example.com']; ['444-555-6666']",
#     "james; []; ['222-333-4444']",
#     "julia; ['julia@example.com']; []",
# ]


# Combine
# 