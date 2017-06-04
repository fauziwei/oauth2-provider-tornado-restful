
1. Install
   $ pip install requirements.txt

2. Start redis-server
   $ sudo /etc/init.d/redis start

3. Run the server
   $ python server.py

4. Insert record for test
   $ python test_insert_db.py

5. Query the record
   $ python test_query_db.py

6. Request new token and save into redis for 1 day expire.
   also for test, the access_token will be saved in file 'access_token.txt'
   $ python test/get_token_oauth2.py

7. $ python test/get_roles.py

8. $ python test/get_users.py

9. $ python test/get_clients.py


For more details how to post/create record in db,
see in 'test' directory:
- test/post_role.py
- test/post_user.py
- test/post_client.py
