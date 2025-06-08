#!/bin/bash
sudo service http-mock stop
git pull
sudo service http-mock start
sudo service http-mock status
