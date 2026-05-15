#!/bin/bash

mkdir -p backups

cp items.db backups/items-$(date +%F-%H-%M).db