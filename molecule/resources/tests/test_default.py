import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '../default/.molecule/ansible_inventory.yml').get_hosts('all')


def test_kapacitor_running(Service):
    kapacitor = Service("kapacitor")
    assert kapacitor.is_running


def test_kapacitor_enabled(Service):
    kapacitor = Service("kapacitor")
    assert kapacitor.is_enabled


@pytest.mark.parametrize("teststring", [
    ('test_db = \\["rp_test_db"\\]'),
    ('test_db_2 = \\["rp_test_db_one", "rp_test_db_two"\\]'),
    ('https-certificate = "/etc/ssl/kapacitor.pem"'),
    ('log-enabled = true'),
    ('write-tracing = false'),
    ('pprof-enabled = false'),
    ('ttps-enabled = false'),
    ('stats-interval = "10s"'),
    ('database = "_kapacitor"'),
    ('retention-policy= "default"'),
    ('url = "https://usage.influxdata.com"'),
    ('dir = "/var/lib/kapacitor/replay"'),
    ('dir = "/var/lib/kapacitor/tasks"'),
    ('snapshot-interval = "60s"'),
    ('boltdb = "/var/lib/kapacitor/kapacitor.db"'),
    ('file = "/var/log/kapacitor/kapacitor.log"'),
    ('level = "INFO"'),
    ('urls = \\["http://localhost:8086"\\]')
])
def test_kapacitor_config(File, teststring):
    kap_config = File("/etc/kapacitor/kapacitor.conf")
    assert kap_config.exists
    assert kap_config.contains(teststring)


def test_tick_file(File):
    for alert in (
        "cpu_alert",
        "disk_alert",
        "cpu_alert_batch"
    ):
        tick_script = File("/tmp/" + alert + ".tick")
        assert tick_script.exists


def test_tick_load(Command):
    tick_load = Command("kapacitor list tasks")
    for alert in (
            "cpu_alert",
            "disk_alert",
            "cpu_alert_batch"
    ):
        assert alert in tick_load.stdout


def test_kapacitor_listener(Socket, SystemInfo):
    assert Socket('tcp://:::9092').is_listening
