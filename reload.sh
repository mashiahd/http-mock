#!/bin/bash
sudo service http-monitor stop
git pull
sudo service http-monitor start
sudo service http-monitor status
