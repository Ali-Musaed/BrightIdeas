SELECT * FROM users left JOIN likes ON users.id = likes.user_id;


DELETE FROM likes where post_id =8;


UPDATE posts SET likes = 4 WHERE posts.id = 14;

SELECT * FROM users Left JOIN posts ON posts.user_id = users.id ORDER BY posts.id DESC;

SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC;


SELECT count(likes.user_id) FROM users JOIN likes ON users.id = likes.user_id WHERE likes.post_id = 15;

INSERT INTO posts (content, user_id) VALUES('An application that searches all the information of a person for job requirements!', 8);


SELECT users.id, count(likes.user_id) FROM users
                JOIN likes ON users.id = likes.user_id
                where user_id = 10;
                
select posts.id, count(likes.user_id) from posts Join likes ON likes.post_id = posts.id where posts.id = 12;
