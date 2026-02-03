RECON_MODULES = {
    "scanner/http/http_version",
    "scanner/http/http_header",
    "scanner/http/http_hsts",
    "scanner/http/title",
    "scanner/http/options",
    "scanner/http/robots_txt",
    "scanner/http/dir_scanner",
    "scanner/http/dir_listing",
    "scanner/http/files_dir",
    "scanner/http/git_scanner",
    "scanner/http/vhost_scanner",
    "scanner/http/enum_wayback",
}

GENERIC_WEB_VULNS = {
    "scanner/http/error_sql_injection",
    "scanner/http/blind_sql_query",
    "scanner/http/host_header_injection",
    "scanner/http/http_put",
    "scanner/http/trace",
    "scanner/http/nginx_source_disclosure",
    "scanner/http/apache_normalize_path",
    "scanner/http/iis_shortname_scanner",
    "scanner/http/log4shell_scanner",
    "scanner/http/graphql_introspection_scanner",
}

WORDPRESS_MODULES = {
    "scanner/http/wordpress_scanner",
    "scanner/http/wordpress_login_enum",
    "scanner/http/wordpress_xmlrpc_login",
    "scanner/http/wp_*",
}

CMS_MODULES = {
    "scanner/http/joomla_scanner",
    "scanner/http/drupal_scanner",
    "scanner/http/magento_scanner",
    "scanner/http/vbulletin_scanner",
}

PROFILES = {
    "recon": RECON_MODULES,
    "standard": RECON_MODULES | GENERIC_WEB_VULNS,
    "full": RECON_MODULES | GENERIC_WEB_VULNS | WORDPRESS_MODULES | CMS_MODULES,
    "wordpress": WORDPRESS_MODULES,
    "cms": CMS_MODULES,
}