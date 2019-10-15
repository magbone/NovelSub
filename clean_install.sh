#!/bin/bash

echo "Clean all installation files..."

BUILD="./build/"
DIST="./dist/"
EGG_INFO="./novelsub.egg-info"

echo "remove $BUILD"
rm -rf $BUILD
echo "remove $DIST"
rm -rf $DIST
echo "remove $EGG_INFO"
rm -rf $EGG_INFO