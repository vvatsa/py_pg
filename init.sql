CREATE EXTENSION multicorn;
create SERVER dds FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.dummy_fdw.DummyFDW');
