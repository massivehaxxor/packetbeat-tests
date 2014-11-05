from pbtests.packetbeat import TestCase


class Test(TestCase):

    def tutorial_asserts(self, objs):
        assert len(objs) == 17
        assert all([o["type"] == "thrift" for o in objs])

        assert objs[0]["thrift"]["request"]["method"] == "ping"
        assert objs[0]["thrift"]["request"]["params"] == "()"
        assert objs[0]["thrift"]["reply"]["returnValue"] == ""

        assert objs[1]["thrift"]["request"]["method"] == "add"
        assert objs[1]["thrift"]["request"]["params"] == "(1: 1, 2: 1)"
        assert objs[1]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[2]["thrift"]["request"]["method"] == "add16"
        assert objs[2]["thrift"]["request"]["params"] == "(1: 1, 2: 1)"
        assert objs[2]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[3]["thrift"]["request"]["method"] == "add64"
        assert objs[3]["thrift"]["request"]["params"] == "(1: 1, 2: 1)"
        assert objs[3]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[4]["thrift"]["request"]["method"] == "add_doubles"
        assert objs[4]["thrift"]["request"]["params"] == "(1: 1.2, 2: 1.3)"
        assert objs[4]["thrift"]["reply"]["returnValue"] == "2.5"

        assert objs[5]["thrift"]["request"]["method"] == "echo_bool"
        assert objs[5]["thrift"]["request"]["params"] == "(1: true)"
        assert objs[5]["thrift"]["reply"]["returnValue"] == "true"

        assert objs[6]["thrift"]["request"]["method"] == "echo_string"
        assert objs[6]["thrift"]["request"]["params"] == "(1: \"hello\")"
        assert objs[6]["thrift"]["reply"]["returnValue"] == "\"hello\""

    def test_thrift_tutorial_socket(self):
        self.render_config_template(
            thrift_ports=[9090]
        )
        self.run_packetbeat(pcap="thrift_tutorial.pcap",
                            debug_selectors=["thrift"])

        objs = self.read_output()

        self.tutorial_asserts(objs)

    def test_thrift_tutorial_framed(self):
        self.render_config_template(
            thrift_ports=[9090],
            thrift_transport_type="framed"
        )
        self.run_packetbeat(pcap="thrift_tutorial_framed_transport.pcap",
                            debug_selectors=["thrift"])

        objs = self.read_output()

        self.tutorial_asserts(objs)

    def test_thrift_tutorial_with_idl(self):
        self.render_config_template(
            thrift_ports=[9091],
            thrift_idl_files=["tutorial.thrift", "shared.thrift"]
        )
        self.copy_files(["tutorial.thrift", "shared.thrift"])
        self.run_packetbeat(pcap="thrift_tutorial.pcap",
                            debug_selectors=["thrift"])

        objs = self.read_output()
        assert len(objs) == 17
        assert all([o["type"] == "thrift" for o in objs])

        assert objs[0]["thrift"]["request"]["method"] == "ping"
        assert objs[0]["thrift"]["request"]["params"] == "()"
        assert objs[0]["thrift"]["reply"]["returnValue"] == ""

        assert objs[1]["thrift"]["request"]["method"] == "add"
        assert objs[1]["thrift"]["request"]["params"] == "(num1: 1, num2: 1)"
        assert objs[1]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[2]["thrift"]["request"]["method"] == "add16"
        assert objs[2]["thrift"]["request"]["params"] == "(num1: 1, num2: 1)"
        assert objs[2]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[3]["thrift"]["request"]["method"] == "add64"
        assert objs[3]["thrift"]["request"]["params"] == "(num1: 1, num2: 1)"
        assert objs[3]["thrift"]["reply"]["returnValue"] == "2"

        assert objs[4]["thrift"]["request"]["method"] == "add_doubles"
        assert objs[4]["thrift"]["request"]["params"] == \
            "(num1: 1.2, num2: 1.3)"
        assert objs[4]["thrift"]["reply"]["returnValue"] == "2.5"

        assert objs[5]["thrift"]["request"]["method"] == "echo_bool"
        assert objs[5]["thrift"]["request"]["params"] == "(b: true)"
        assert objs[5]["thrift"]["reply"]["returnValue"] == "true"

        assert objs[6]["thrift"]["request"]["method"] == "echo_string"
        assert objs[6]["thrift"]["request"]["params"] == "(s: \"hello\")"
        assert objs[6]["thrift"]["reply"]["returnValue"] == "\"hello\""
