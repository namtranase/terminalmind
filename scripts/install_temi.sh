#!/bin/bash
dpkg-deb --build temi-packaging temi.deb
sudo dpkg -i temi.deb