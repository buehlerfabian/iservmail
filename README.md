#  IServ-Mail

A simple local web server that forwards incoming emails via the Iserv webmail interface. It can be used when STMP access is blocked in the Iserv configuration.

## Configuration
Create a file named `config.py` with your Iserv credentials:
```
iserv_username = 'my.username'
iserv_password = 'MyPassword'
iserv_url = 'https://iserv-url.xyz'
iserv_allowed_domain = 'iserv-url.xyz'
``` 

The Iserv installation at my school only allows sending mails to internal addresses, i.e. to other Iserv users. `iserv_allowed_domain` specifies the valid domain, mails to other domains will be rejected. Currently this feature cannot be disabled.

## Additional configuration for tests
If you want to run the development tests, create an additional config file named `config_tests.py`:
```
iserv_full_username = 'My Name'
iserv_address_for_test = 'test.address@my-iserv.xyz'
outside_address_for_test = 'outside.adress@other.domain'
```
Them mail to the address specified under `outside_address_for_test`  is currently rejected, but that will likely change in the future. So you may want to specify one of your own email addresses here.