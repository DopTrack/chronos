# Add doptrackwebappserver to running services
#
# Assuming the user is "doptrack"
#
cp "init.d/webappservercontrol" "/etc/init.d/doptrackwebappserver"
chmod +x /etc/init.d/doptrackwebappserver
touch "/var/log/doptrackwebappserver.log"
touch "/var/log/pythonDoptrackServer.log"
update-rc.d "doptrackwebappserver" defaults
service doptrackwebappserver start