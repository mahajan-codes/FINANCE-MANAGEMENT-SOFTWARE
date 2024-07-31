# FINANCE-MANAGEMENT-SOFTWARE

Hi, I developed innovative software to manage multiple businesses simultaneously using Tally accounting software. Tally is a popular choice for business finance management but has a limitation: it handles companies individually. My solution overcomes this by connecting a web application running on a Flask server to Tally.

When a contract is entered on the web application, it seamlessly integrates with Tally using RabbitMQ and Celery. As soon as billing is completed in Tally, my software updates the web application and database, making it efficient to manage multi-million dollar finances across multiple businesses.

Tools used include: Flask, RabbitMQ, Celery, SQLite, AWS, XML, ODBC interface and Test cases.
