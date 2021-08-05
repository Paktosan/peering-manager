# Policies
Peering Manager allows _routing policies_ to be defined. These policies can then be applied to:
* Autonomous Systems
* Internet Exchanges
  * Internet Exchange Peering Sessions
* BGP Groups
  * Direct Peering Sessions

First, these policies defined in Peering Manager must be exported via template to the router, then they need to be applied to prefixes received or announced.

!!!attention
    How policies are handled by templates shown here is pretty much work in progress. Ideas how your templates handle policies are very much welcome.

=== "Cisco IOS XR"
    We dump simply the content of the policy into a _route-policy_ statement. This makes the whole process completely dependend on the router platform.


    ```
    {%- for policy in routing_policies %}
    !
    route-policy {{policy.name}}
      {%- if policy.config_context is iterable %}
        {%- for statement in policy.config_context %}
          {#- Simply dump all statements one after another#}
          {{statement}}
        {%-endfor%}
      {%-endif%}
    end-policy
    {%-endfor%}
    ```
=== "Cisco IOS"
    This does not work on IOS.


An idea would be to use _tags_ to mark which policies can be applied on which router platform.

Alternatively the JSON _Config Context_ of the policy can be used to encode different policies for different platforms:
```JSON
{
  "iosxr": {
    "statements": [
    "set local-preference 10000",
    "pass"
    ]
  },
  "ios": {
    "order":100,
    "result":"permit",
    "statements": [
      "set local-preference 10000"
    ]
  }
}

```
