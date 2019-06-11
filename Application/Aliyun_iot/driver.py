#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from linkkit import linkkit


class Example(object):
    def __init__(self, debug=True):
        self.debug = debug

        self.host_name = 'cn-shanghai'
        self.product_key = 'a1EW5CuFNEc'
        self.device_name = 'FxDuAY9QGDWxogkyKL8Z'
        self.device_secret = 'aiF4DjBH3lj3BhOL2rLGJxegFYltv4Gh'

        self.alink_topic_update = '/sys/{}/{}/thing/event/property/post'.format(self.product_key, self.device_name)

        self.lk = linkkit.LinkKit(
            host_name=self.host_name,
            product_key=self.product_key,
            device_name=self.device_name,
            device_secret=self.device_secret
        )
        self.lk.config_mqtt()
        self.lk.config_device_info('RisingHF|Computer')

        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        self.lk.on_subscribe_topic = self.on_subscribe_topic
        self.lk.on_unsubscribe_topic = self.on_unsubscribe_topic
        self.lk.on_publish_topic = self.on_publish_topic
        self.lk.on_topic_message = self.on_topic_message

        self.lk_connect = False
        self.lk_send = False
        self.lk.connect_async()

        while not self.lk_connect:
            pass

        self.temp = 30.0
        while True:
            sleep(5)
            _params = '{\"Name\":\"%s\",\"Version\":\"%s\",\"Temperature\":%.1f}' % ('rxhf', '0.0.1', self.temp)
            _data = '{\"id\":\"123\",\"version\":\"1.0\",\"method\":\"thing.event.property.post\",\"params\":%s}' % _params
            self.do_publish_topic(
                self.alink_topic_update,
                _data
            )
            self.temp += 0.5

    def on_connect(self, session_flag, rc, data):
        self.lk_connect = True
        if not self.debug:
            return
        print('on_connect:session_flag={}, rc={}, data:{}'.format(
            session_flag, rc, data
        ))

    def on_disconnect(self, rc, data):
        self.lk_connect = False
        if not self.debug:
            return
        print('on_disconnect:rc={}, data:{}'.format(
            rc, data
        ))

    def on_subscribe_topic(self, mid, qos, data):
        if not self.debug:
            return
        # qos 为订阅topic列表对应的qos返回结果，正常值为0或1，128表示订阅失败
        print('on_subscribe_topic mid:{}, qos:{}, data:{}'.format(
            mid, str(','.join('%s' % it for it in qos)), data
        ))

    def on_unsubscribe_topic(self, mid, data):
        if not self.debug:
            return
        # 回调on_unsubscribe_topic时表明取消成功
        print('on_unsubscribe_topic mid:{},data:{}'.format(
            mid, data
        ))

    def on_publish_topic(self, mid, data):
        self.lk_send = True
        if not self.debug:
            return
        # 回调on_publish_topic 表明publish成功
        print('on_publish_topic mid:{},data:{}'.format(
            mid, data
        ))

    def on_topic_message(self, topic, payload, qos, data):
        if not self.debug:
            return
        print('on_topic_message:topic:{}, payload:{}, qos:{}, data:{}'.format(
            topic, payload, qos, data
        ))

    def do_subscribe_topic(self, topic):
        # subscribe_topic 返回值rc 为0表明请求已写入缓存区，其它值失败
        return self.lk.subscribe_topic(topic)

    def do_unsubscribe_topic(self, topic):
        # unsubscribe_topic 返回值rc 为0表明请求已写入缓存区，其它值失败
        return self.lk.unsubscribe_topic(topic)

    def do_publish_topic(self, topic, msg):
        # publish_topic rc返回值为0则表明已经写入到了发送缓冲区
        return self.lk.publish_topic(topic, msg)


if __name__ == '__main__':
    ex = Example()
