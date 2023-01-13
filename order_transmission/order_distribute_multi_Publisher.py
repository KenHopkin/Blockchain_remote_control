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
order_distribute Publisher
"""
from threading import Condition
import time
import datetime

import fastdds
import order_distribute

DESCRIPTION = """OrderDistribute Publisher example for Fast DDS python bindings"""
USAGE = ('python3 order_distributePublisher.py')
summessage = 0


class WriterListener (fastdds.DataWriterListener) :
    def __init__(self, writer) :
        self._writer = writer
        super().__init__()

    def on_publication_matched(self, datawriter, info) :
        if (0 < info.current_count_change) :
            print ("Publisher matched subscriber {}".format(info.last_subscription_handle))
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader += 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()
        else :
            print ("Publisher unmatched subscriber {}".format(info.last_subscription_handle))
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader -= 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()



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
        global summessage
        summessage = summessage + 1



class Writer:


    def __init__(self):
        self._matched_reader = 0
        self._cvDiscovery = Condition()
        self.index = 0

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
        self.Writer_topic = self.participant.create_topic("OrderDistributeTopic_xie2", self.topic_data_type.getName(), self.topic_qos)
        self.Reader_topic = self.participant.create_topic("OrderDistributeTopic_xie_collection", self.topic_data_type.getName(),
                                                          self.topic_qos)

        self.publisher_qos = fastdds.PublisherQos()
        self.participant.get_default_publisher_qos(self.publisher_qos)
        self.publisher = self.participant.create_publisher(self.publisher_qos)

        self.subscriber_qos = fastdds.SubscriberQos()
        self.participant.get_default_subscriber_qos(self.subscriber_qos)
        self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

        self.writer_listener = WriterListener(self)
        self.writer_qos = fastdds.DataWriterQos()
        self.publisher.get_default_datawriter_qos(self.writer_qos)
        self.writer = self.publisher.create_datawriter(self.Writer_topic, self.writer_qos, self.writer_listener)

        self.Reader_listener = ReaderListener()
        self.reader_qos = fastdds.DataReaderQos()
        self.subscriber.get_default_datareader_qos(self.reader_qos)
        self.reader = self.subscriber.create_datareader(self.Reader_topic, self.reader_qos, self.Reader_listener)

    def write(self):
        data = order_distribute.OrderDistribute()
        data.message("please start the mission")
        data.index(self.index)
        self.writer.write(data)
        print("Sending {message} : {index}".format(message=data.message(), index=data.index()))
        self.index = self.index + 1


    def wait_discovery(self) :
        self._cvDiscovery.acquire()
        print ("Writer is waiting discovery...")
        self._cvDiscovery.wait_for(lambda : self._matched_reader != 0)
        self._cvDiscovery.release()
        print("Writer discovery finished...")


    def run(self):
        self.wait_discovery()
        for x in range(10) :
            time.sleep(1)
            self.write()
        global summessage
        while summessage <= 0:
            time.sleep(1)
            print(summessage)

        self.delete()


    def delete(self):
        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant.delete_contained_entities()
        factory.delete_participant(self.participant)


if __name__ == '__main__':
    print('Starting publisher.')
    writer = Writer()
    writer.run()
    exit()
