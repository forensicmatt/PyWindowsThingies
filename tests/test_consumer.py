import time
import unittest
from winthingies.win32.const import EVENT_TRACE_FLAG_REGISTRY
from winthingies.trace import TraceProvider
from winthingies.trace import TraceSession
from winthingies.trace import TraceConsumer


class TestProvider(unittest.TestCase):
    def test_kernel_provider(self):
        provider_kernel_trace = TraceProvider(
            u"Windows Kernel Trace",
            u"{9E814AAD-3204-11D2-9A82-006008A86939}",
            match_any_keyword=EVENT_TRACE_FLAG_REGISTRY
        )
        t_session = TraceSession(
            u"NT Kernel Logger",
            [provider_kernel_trace]
        )
        t_session.start()

        t_consumer = TraceConsumer(
            u"NT Kernel Logger",
            None
        )
        t_consumer.start()

        timer = time.time() + 10
        while time.time() < timer:
            pass
        t_consumer.stop()

        # wait for consumer to exit
        t_consumer.join()

        t_session.stop()

    def test_other_provider(self):
        provider_kernel_trace = TraceProvider(
            u"Microsoft-Windows-Kernel-Registry",
            u"{70EB4F03-C1DE-4F73-A051-33D13D5413BD}"
        )

        t_session = TraceSession(
            u"Test 1",
            [provider_kernel_trace]
        )
        t_session.start()

        t_consumer = TraceConsumer(
            u"Test 1",
            None
        )
        t_consumer.start()

        timer = time.time() + 10
        while time.time() < timer:
            pass
        t_consumer.stop()

        # wait for consumer to exit
        t_consumer.join()

        t_session.stop()


if __name__ == '__main__':
    unittest.main()
