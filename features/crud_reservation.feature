Feature: Reservation

  Background:
    Given create the test database
    And user1 input a citizen_id: "1152347583215" to create
    And user1 input a password: "test password" to create
    When user1 send a request to create a user
    Given user1 input a citizen_id: "1152347583215" to login
    And user1 input a password: "test password" to login
    When user1 send a request to login

  Scenario: simple create reservation
    Given user1 input a timestamp: "27/10/2021" to create reservation
    When user1 send a request to create reservation
    Then website send status code "201" to user1 from create reservation
    Then tear down database

  Scenario: simple get reservation
    Given user1 input a timestamp: "27/10/2021" to create reservation
    When user1 send a request to create reservation
    When user1 send a request to get a reservation id: "1"
    Then website send status code "200" to user1 from get reservation
    Then tear down database

  Scenario: simple update reservation
    Given user1 input a timestamp: "27/10/2021" to create reservation
    When user1 send a request to create reservation
    Given user1 input a new timestamp: "1/11/2021" to update reservation
    When user1 send a request to update reservation id: "1"
    Then website send status code "200" to user1 from update reservation
    Then tear down database

  Scenario: simple delete reservation
    Given user1 input a timestamp: "27/10/2021" to create reservation
    When user1 send a request to create reservation
    When user1 send a request to delete a reservation id: "1"
    Then website send status code "200" to user1 from delete reservation
    Then tear down database