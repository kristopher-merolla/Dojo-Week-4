-- 1. What query would you run to get the total revenue for March of 2012?
select SUM(billing.amount) AS 'Total Revenue for Mar 2012'
from lead_gen_business.billing
where charged_datetime > '2012-02-01';
-- 
-- 2. What query would you run to get total revenue collected from the client with an id of 2?
select billing.client_id, SUM(billing.amount) AS 'Total Revenue for Mar 2012'
from lead_gen_business.billing
where billing.client_id = 2;
-- 
-- 3. What query would you run to get all the sites that client=10 owns?
select sites.client_id, sites.domain_name
from lead_gen_business.sites
where sites.client_id = 10;
-- 
-- 4. What query would you run to get total number of sites created per month per year for 
-- the client with an id of 1? What about for client=20?
-- per month
select sites.client_id, count(sites.domain_name), month(sites.created_datetime)
from lead_gen_business.sites
where sites.client_id in (1,20)
group by month(sites.created_datetime);
-- per year
select sites.client_id, count(sites.domain_name), year(sites.created_datetime)
from lead_gen_business.sites
where sites.client_id in (1,20) 
group by year(sites.created_datetime);
-- 
-- 5. What query would you run to get the total 
-- # of leads generated for each of the sites between January 1, 2011 to February 15, 2011?
select sites.domain_name, COUNT(leads.site_id) AS 'Leads between Jan 1, 2011 and Feb 15, 2011'
from lead_gen_business.sites
left join lead_gen_business.leads on leads.site_id = sites.site_id
and '2011-01-01' < leads.registered_datetime < '2011 02 15' 
group by sites.domain_name;
-- 
-- 6. What query would you run to get a list of client names and the total 
-- # of leads we've generated for each of our clients between January 1, 2011 to December 31, 2011?
select CONCAT(clients.first_name, clients.last_name) AS 'Client Name', 
COUNT(leads.site_id) AS 'Leads between Jan 1, 2011 and Dec 31, 2011'
from lead_gen_business.clients
left join lead_gen_business.sites on sites.client_id = clients.client_id
left join lead_gen_business.leads on leads.site_id = sites.site_id
and '2011-01-01' < leads.registered_datetime < '2011 12 31' 
group by CONCAT(clients.first_name, clients.last_name);
-- 
-- 7. What query would you run to get a list of client names and the total 
-- # of leads we've generated for each client each month between months 1 - 6 of Year 2011?
select month(leads.registered_datetime), CONCAT(clients.first_name, clients.last_name) AS 'Client Name', 
COUNT(leads.site_id) AS 'Leads between Jan 1, 2011 and Jun 30, 2011'
from lead_gen_business.clients
left join lead_gen_business.sites on sites.client_id = clients.client_id
left join lead_gen_business.leads on leads.site_id = sites.site_id
and year(leads.registered_datetime) = 2011
and month(leads.registered_datetime) < 7
group by CONCAT(clients.first_name, clients.last_name);
-- 
-- 8. What query would you run to get a list of client names and the total 
-- # of leads we've generated for each of our clients' sites between January 1, 2011 to December 31, 2011? 
-- Order this query by client id.  Come up with a second query that shows all the clients, 
-- the site name(s), and the total number of leads generated from each site for all time.
-- 
-- 9. Write a single query that retrieves total revenue collected from each client for each month of the year. 
-- Order it by client id.
-- 
-- 10. Write a single query that retrieves all the sites that each client owns. 
-- Group the results so that each row shows a new client. 
-- It will become clearer when you add a new field called 'sites' that has all the sites that the client owns. 
-- (HINT: use GROUP_CONCAT)
