Feature: User login

  Background:
    Given create the test database
    And user1 input a citizen_id: "1152347583215" to create
    And user1 input a password: "test password" to create
    When user1 send a request to create a user

  Scenario: simple login
    Given user1 input a citizen_id: "1152347583215" to login
    And user1 input a password: "test password" to login
    When user1 send a request to login
    Then website send status code "200" to user1 from login
    Then tear down database

  Scenario: try to login with incorrect password
    Given user1 input a citizen_id: "1152347583215" to login
    And user1 input a password: "not a test password" to login
    When user1 send a request to login
    Then website send status code "404" to user1 from login
    Then tear down database

  Scenario: try to login with user that does not exist
    Given user1 input a citizen_id: "1152347583000" to login
    And user1 input a password: "test password" to login
    When user1 send a request to login
    Then website send status code "404" to user1 from login
    Then tear down database
    
    