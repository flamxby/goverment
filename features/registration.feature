Feature: Registration

  Scenario: create user
    Given create the test database
    And user1 input a citizen_id: "1152347583215" to create
    When user1 send a request to create a user
    Then website send status code "201" to user1
    Then tear down database

  Scenario: try to register with duplicate citizen id
    Given create the test database
    And user1 input a citizen_id: "1152347583215" to create
    And user2 input a citizen_id: "1152347583215" to create
    When user1 send a request to create a user
    When user2 send a request to create a user
    Then website send status code "201" to user1
    Then Has an error for create user2
    Then tear down database
