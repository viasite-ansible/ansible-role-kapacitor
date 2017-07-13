import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_kapacitor_running_and_enabled(Service):
    kapacitor = Service("kapacitor")
    assert kapacitor.is_running
    assert kapacitor.is_enabled


def test_kapacitor_config(File):
    kap_config = File("/etc/kapacitor/kapacitor.conf")
    assert kap_config.exists
    assert kap_config.contains('test_db = \\["rp_test_db"\\]')
    assert kap_config.contains('test_db_2 = ' +
                               '\\["rp_test_db_one", "rp_test_db_two"\\]')


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
