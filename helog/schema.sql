drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    user string not null,
    meter string not null,
    meter_before integer not null,
    meter_after integer not null,
    transport_dewar string not null,
    transport_dewar_before integer not null,  
    transport_dewar_after integer not null,  
    cryostat string not null,
    ip string not null,
    misc string,
    time timestamp not null
);

