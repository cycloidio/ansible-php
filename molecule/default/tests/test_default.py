import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    php_version = host.ansible.get_variables()["php_version_to_install"]
    if php_version == 5:
        present = [
            "/etc/php{}".format(php_version),
            "/etc/php{}/cli".format(php_version),
            "/etc/php{}/cli/conf.d".format(php_version),
            "/etc/php{}/fpm".format(php_version),
            "/etc/php{}/fpm/conf.d".format(php_version),
            "/etc/php{}/fpm/pool.d".format(php_version),
        ]
    else:
        present = [
            "/etc/php/{}".format(php_version),
            "/etc/php/{}/cli".format(php_version),
            "/etc/php/{}/cli/conf.d".format(php_version),
            "/etc/php/{}/fpm".format(php_version),
            "/etc/php/{}/fpm/conf.d".format(php_version),
            "/etc/php/{}/fpm/pool.d".format(php_version),
        ]
    if present:
        for directory in present:
            d = host.file(directory)
            assert d.is_directory
            assert d.exists


def test_files(host):
    php_version = host.ansible.get_variables()["php_version_to_install"]
    if php_version == 5:
        present = [
            "/etc/php{}/cli/php.ini".format(php_version),
            "/etc/php{}/cli/conf.d/05-opcache.ini".format(php_version),
            "/etc/php{}/fpm/php.ini".format(php_version),
            "/etc/php{}/fpm/conf.d/05-opcache.ini".format(php_version),
            "/etc/php{}/fpm/pool.d/www-data.conf".format(php_version)
        ]
    else:
        present = [
            "/etc/php/{}/cli/php.ini".format(php_version),
            "/etc/php/{}/cli/conf.d/05-opcache.ini".format(php_version),
            "/etc/php/{}/fpm/php.ini".format(php_version),
            "/etc/php/{}/fpm/conf.d/05-opcache.ini".format(php_version),
            "/etc/php/{}/fpm/pool.d/www-data.conf".format(php_version)
        ]
    if present:
        for file in present:
            f = host.file(file)
            assert f.exists
            assert f.is_file


def test_service(host):
    php_version = host.ansible.get_variables()["php_version_to_install"]
    present = [
        "php{}-fpm".format(php_version)
    ]
    if present:
        for service in present:
            s = host.service(service)
            assert s.is_enabled
            assert s.is_running


def test_packages(host):
    php_version = host.ansible.get_variables()["php_version_to_install"]
    present = [
        "php{}".format(php_version),
        "php-pear"
    ]
    if present:
        for package in present:
            p = host.package(package)
            assert p.is_installed
