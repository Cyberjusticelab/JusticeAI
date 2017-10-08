#Classification worksheet

This markdown is used as aid for the classification of the various components regarding the different subjects.
Main articles explored Chapter 4: **1849-2000**
Articles by importance from 1849-2000:
1. Article 1971
2. Article 1883
3. Article 1947
4. Article 1973
5. Article 1975
6. Article 1863
7. Article 1967
8. Article 1963
9. Article 1855
10. Article 1854
 
Articles outside of 1849-2000 whom are also important: (Updated as we make contact with a professional)
1. 
2. 
3. 

##Classification

###State of dwelling:
* Regular Damages to the infrastructure (fire, denting, scratching)
* Damages to the leased furniture
* Electric, Plumbing damages (to be repaired by the landlord if can’t prove it’s the tenants’ fault)


###Deposits (All Illegal yet still exploited - Landlords are pushing for the law to change)
* Key or security deposit
* “Month rent in advance” (Landlord is allowed to rent for a portion of the 1st month rent - Article 1904)

###Lack of payment:
* Being in default after day 1
* Charging interest rates on the delayed payment
* Being at risk of expulsion after 3 weeks
* Finding an old tenant 2 years after the lease was not paid after he left (3 year rule)
* Payment after 3 weeks or after the decision is upheld of eviction (tenant can stay if he pays)

###Breaking the lease
* Leaving before termination of the lease
* Replacing the lessee with other lessee (as tenant or landlord)
* Who pays rent if one lesse leaves in a collocation (do tenants endorse the rest?)
* Individuals breaking the lease when the individual itself is done pursuing studies (special permission for students)

###Renewal and creation of lease
* Limitation on the number of occupants (very vague)
* Information landlord can request (No SIN, Driver’s license, passport, health card, allowed credit check) - Not a lease law but a privacy issue
* Regulation around co-signer for students that cannot prove good paying habits
* Replacing someone against his will at the renewal of the lease (6 months in advance and has 1 month to reply back)
* Regulations regarding subletting (students not allowed? Article 1981)
* Regulations around mobile homes
* Regulations with landlord living with the tenant in the same dwelling
* Regulations of lease of a terrain in respects to a mobile home

###Regulation of landlord visiting
* Regulations of placing visits for the appartment for new tenants
* Agreements of landlord’s access to the apartment

###Repairs
* Regulations on repairs by tenant (if he wants to do it himself, if landlord is not doing it and how to bill the landlord back later)
* Hours of repairs and protocols of interactions with tenants for landlord to be doing the repairs of the apartment

###Habitability
* Regulations of heating of the apartment
* Regulations regarding noise pollution
* Regulations on cleanliness of the apartment
* Regulations around smoking (+ cannabis)
* Regulations around lock changing without advising tenant or giving key
* Regulations around hot water
* Regulations around internet providers as a service (measures)

###Pets
* Dogs and Cats
* Others (different for birds, fishes, etc.)


##Sources:
[Outils de calcul de fixation de loyer](https://www.rdl.gouv.qc.ca/).  
[Code Civil du Quebec](http://legisquebec.gouv.qc.ca/fr/ShowDoc/cs/CCQ-1991). 
[Civil Code of Quebec](http://legisquebec.gouv.qc.ca/en/showdoc/cs/CCQ-1991).  
[Brief rights of tenant/landlord](https://www.rdl.gouv.qc.ca/fr/etre-locataire/droits-et-obligations-du-locataire).  
[FAQ Regie](https://www.rdl.gouv.qc.ca/fr/questions-frequentes).  
[Explanations payment](https://www.rdl.gouv.qc.ca/fr/etre-locataire/paiement-du-loyer).  
[What to do in front of Regie](http://legisquebec.gouv.qc.ca/fr/ShowDoc/cr/R-8.1,%20r.%205).  
[Quick facts from CSU](https://csu.qc.ca/hojo/basic-facts-about-renting-quebec-english-and-mandarin-pdf).  
[Privacy issue SIN/Driver's license, etc.](https://www.rdl.gouv.qc.ca/en/signing-a-lease/the-lease-and-protection-of-personal-information).  

##JSON rough draft format of categories:

This does not necessarily reflect the first categorization articles but will be the same in principle.
The parameter of every category needs to be true for the corresponding text to be relevant to this category.
These categories may become tags as the iteration passes and the full extent of the law regarding La Regie du Logement is understood. 
The facts under every category will be changed according to the programmers' needs.  

It is absolutely **IMPERATIVE** that every category is covered by (optional in parenthesis):

* Who
* What
* When
* Where
* How
* (by who)
* (how much)

###Format (fact_key:fact_type - (optional description))

#####state_of_dwelling (events relating to the damages incurred to a property)


<code>is_damaged:bool (this starts the making of what is below and the categorization itself)</code>


what_is_damaged:list 
value_of_damages:number in list of list (current value)
is_fixable: boolean in list of list (scratch on a wall is fixable, microwave is replaceable)
when_each_damage:dateformat in list of list  
has_picture_before:bool in list of list (if the tenant or landlord has pictures of before the) -- Evidence prompt
how_was_damaged:string in list of list

i.e. 

| What | Fridge | Microwave |
| ------:| -----------:| -----------:|
| Value   | 230  | 90 |
| Fixable | False | False |
| When | 2/13/2017 | 2/15/2017  |
| Proof   | True | False |
| How | Old | Aluminium in Microwave |



#####Create_renew_lease (events created to the renewal or the creation of a lease)

<code>is_new_lease:bool</code>
pay_for_what:[mobile home, home, appartment]

<code>is_exist_deposit:bool</code>  
which_deposit:[payInAdvance, safety, key]

<code>is_asking_proof_if_I_can_pay:bool</code>  
is_ask_for_info:bool (info like SIN, Driver's license, etc.)  
is_ask_if_i_pay:bool (co-signer questions, etc.)

<code>is_asking_roommates:bool</code>
max_number_occupants:number
is_replacing_me_after_lease:bool


#####Landlord_visit (events including any access of the landlord to the premise (repairs and visitation))

<code><is_landlord_visiting:bool></code>
is_repairs:bool
is_visit_new_tenant:bool

#####Habitability (events related to the habitability of an apartment including repairs)

<code>need_repairs:bool</code>  
is_repair_scheduled:bool (goes back to state of dwelling )  

<code>is_noisy:bool</code>  

<code>heating:bool</code>  
since_when_no_heat:dateformat  

<code>has_smoking:bool</code>
which_type:[cannabis, cigarette, other]
is_in_lease:bool (OCR)

<code>is_clean:bool</code>  

<code>has_hot_water:bool</code>  

<code>has_usable_internet:bool</code> (VERY iffy and hard to classify as this is a new thing to include in a lease)

<code>lock_change:bool</code>
advise:string  

#####lease_termination (events related to the premature termination of a lease)

lease_term_type:[indeterminate, fixed]  
has_lease_expired:bool  
is_tenant_dead:bool  
is_student:bool  
is_habitable:bool  

#####Rent_pay (this will include how to pay and deposits)


#####Rent_change (Events related to the change in payment of rent)

lease_term_type:[indeterminate, fixed]  
is_rent_in_lease:bool  
rent_in_lease_amount:number  

#####Rent_nopay (events related to the lack of payment)

in_default:bool (over one day late paying)
over_three_weeks:bool  
has_abandoned:bool  
interest_allowed:bool  
interest_term:number  
interest_max:number  
is_rent_advance:bool  
first_month_rent_paid:bool  

#####Pets (events related to the acquisition or the bringing of non-human companions)
has_pet:bool  
which_pet:[dog, cat, other]

##Questions per category with follow-up structure:

