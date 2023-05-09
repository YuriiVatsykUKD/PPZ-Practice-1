FROM php:8.1.15-apache
#############################################
# environment setup 
#############################################
#create required folders
RUN mkdir -p /var/.tmp
RUN chmod -fR 777 /var/.tmp

#Install necessary packages
RUN apt-get update && \
    apt-get install \
    libssh2-1 \
    libssh2-1-dev \
    wget \
    libssl-dev \
    libzip-dev \
    libpng-dev \
    libpq-dev \
    zip \
    libxml2-dev \
    zlib1g-dev \
    libicu-dev \
    g++ \
    -y --no-install-recommends \
    && docker-php-ext-install zip calendar

#Cleanup packages
RUN apt-get purge -y g++ \
    && apt-get autoremove -y
RUN rm -rf /tmp/* \
    && rm -rf /var/list/apt/* \
    && rm -rf /var/lib/apt/lists/*

#############################################
# apache2 setup 
#############################################
# Copy virtual host into container
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN service apache2 restart

#Enable rewrite mode
RUN a2enmod rewrite

#############################################
# copy app and configurations 
#############################################
# Copy php.ini
COPY ./php.ini $PHP_INI_DIR/conf.d/

# Copy in custom code from the host machine.
WORKDIR /var/www/html
COPY . /var/www/html

# Delete not used config files
RUN rm -f /var/www/html/php.ini \
    && rm -f /var/www/html/000-default.conf

# Change the owner of the container document root
RUN chown -R www-data:www-data /var/www

#Start Apache in foreground
CMD ["apache2-foreground"]