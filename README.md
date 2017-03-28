# TestSberCalc
This repo includes selenium tests for
sberbank exchange calc

How to install and run tests:

Install chrome webdriver like said here:
http://blog.likewise.org/2015/01/setting-up-chromedriver-and-the-selenium-webdriver-python-bindings-on-ubuntu-14-dot-04/

Install venv and packages:
1) sudo apt-get install virtualenv
2) virtualenv <env_name>
3) cd <project_root_dir>
3) . ./<env_name>/bin/activate
4) pip install -r requirements.txt

Run tests with command: pytest --alluredir=/var/tmp/allure/ -v -m test_currency under project dir

Get report
1) Get the latest allure package
wget https://github.com/allure-framework/allure1/releases/download/allure-core-1.5.2/allure-commandline.tar.gz
2) untar to some folder
3) make report with ./allure generate report /var/tmp/allure 
4) open report: ./allure report open
