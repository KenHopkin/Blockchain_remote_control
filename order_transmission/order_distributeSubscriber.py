# Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
order_distribute Subscriber
"""
import signal

import fastdds
import order_distribute

DESCRIPTION = """OrderDistribute Subscriber example for Fast DDS python bindings"""
USAGE = ('python3 order_distributeSubscriber.py')

# To capture ctrl+C
def signal_handler(sig, frame):
    print('Interrupted!')

class ReaderListener(fastdds.DataReaderListener):


    def __init__(self):
        super().__init__()


    def on_subscription_matched(self, datareader, info) :
        if (0 < info.current_count_change) :
            print ("Subscriber matched publisher {}".format(info.last_publication_handle))
        else :
            print ("Subscriber unmatched publisher {}".format(info.last_publication_handle))


    def on_data_available(self, reader):
        info = fastdds.SampleInfo()
        data = order_distribute.OrderDistribute()
        reader.take_next_sample(data, info)

        print("Received {message} : {index}".format(message=data.message(), index=data.index()))


class Reader:


    def __init__(self):
        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant_qos = fastdds.DomainParticipantQos()
        factory.get_default_participant_qos(self.participant_qos)
        self.participant = factory.create_participant(0, self.participant_qos)

        self.topic_data_type = order_distribute.OrderDistributePubSubType()
        self.topic_data_type.setName("order_distribute_hiahia")
        self.type_support = fastdds.TypeSupport(self.topic_data_type)
        self.participant.register_type(self.type_support)

        self.topic_qos = fastdds.TopicQos()
        self.participant.get_default_topic_qos(self.topic_qos)
        self.topic = self.participant.create_topic("OrderDistributeTopic_xie2", self.topic_data_type.getName(), self.topic_qos)

        self.subscriber_qos = fastdds.SubscriberQos()
        self.participant.get_default_subscriber_qos(self.subscriber_qos)
        self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

        self.listener = ReaderListener()
        self.reader_qos = fastdds.DataReaderQos()
        self.subscriber.get_default_datareader_qos(self.reader_qos)
        self.reader = self.subscriber.create_datareader(self.topic, self.reader_qos, self.listener)


    def delete(self):
        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant.delete_contained_entities()
        factory.delete_participant(self.participant)


    def run(self):
        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to stop')
        signal.pause()
        self.delete()


if __name__ == '__main__':
    print('Creating subscriber.')
    reader = Reader()
    reader.run()
    exit()
