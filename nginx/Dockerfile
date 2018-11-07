FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default
COPY praylink.conf /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/praylink.conf /etc/nginx/sites-enabled/praylink.conf
