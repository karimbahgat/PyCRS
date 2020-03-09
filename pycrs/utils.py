"""
Misc utility functions related to crs formats and online services. 
"""

try:
    import urllib.request as urllib2
    from urllib.parse import urlencode
except ImportError:
    import urllib2
    from urllib import urlencode
import re
import json

EPSG_URL = 'http://prj2epsg.org/search.json'


def build_crs_table(savepath):
    """
    Build crs table of all equivalent format variations by scraping spatialreference.org.
    Saves table as tab-delimited text file.
    NOTE: Might take a while.

    Arguments:

    - *savepath*: The absolute or relative filepath to which to save the crs table, including the ".txt" extension. 
    """
    # create table
    outfile = open(savepath, "wb")
    
    # create fields
    fields = ["codetype", "code", "proj4", "ogcwkt", "esriwkt"]
    outfile.write("\t".join(fields) + "\n")
    
    # make table from url requests
    for codetype in ("epsg", "esri", "sr-org"):
        print(codetype)
        
        # collect existing proj list
        print("fetching list of available codes")
        codelist = []
        page = 1
        while True:
            try:
                link = 'https://spatialreference.org/ref/%s/?page=%s' %(codetype,page)
                html = urllib2.urlopen(link).read()
                codes = [match.groups()[0] for match in re.finditer(r'/ref/'+codetype+'/(\d+)', html) ]
                if not codes: break
                print("page",page)
                codelist.extend(codes)
                page += 1
            except:
                break

        print("fetching string formats for each projection")
        for i,code in enumerate(codelist):
            
            # check if code exists
            link = 'https://spatialreference.org/ref/%s/%s/' %(codetype,code)
            urllib2.urlopen(link)
            
            # collect each projection format in a table row
            row = [codetype, code]
            for resulttype in ("proj4", "ogcwkt", "esriwkt"):
                try:
                    link = 'https://spatialreference.org/ref/%s/%s/%s/' %(codetype,code,resulttype)
                    result = urllib2.urlopen(link).read()
                    row.append(result)
                except:
                    pass

            print("projection %i of %i added" %(i,len(codelist)) )
            outfile.write("\t".join(row) + "\n")

    # close the file
    outfile.close()

            
def crscode_to_string(codetype, code, format):
    """
    Lookup crscode and return in specified format.
    Uses epsg.io for epsg code, or spatialreference.org for esri or sr codes.

    Arguments:

    - *codetype*: "epsg", "esri", or "sr-org".
    - *code*: The code.
    - *format*: The crs format of the returned string. One of "ogcwkt", "esriwkt", or "proj4", but also several others...

    Returns:

    - Crs string in the specified format. 
    """
    if codetype == 'epsg':
        # use epsg.io which is more up-to-date, but can only lookup epsg codes
        if format == 'ogcwkt':
            format = 'wkt'
        link = 'https://epsg.io/{}.{}'.format(code, format)
        req = urllib2.Request(link, headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
        result = urllib2.urlopen(req).read()
    else:
        # use spatialreference.org
        link = 'https://spatialreference.org/ref/{}/{}/{}/'.format(codetype,code,format)
        result = urllib2.urlopen(link).read()
    if not isinstance(result, str):
        result = result.decode()
    return result


def wkt_to_epsg(wkt):
    """ Lookup the EPSG code of a particular WKT projection.

    Returns the results dictionary from http://prj2epsg.org, with the
    following key entries:

    - exact: true if the provided WKT could be matched exactly to one entry in the EPSG database, false otherwise
    - totalHits: total amount of potential results found in the database. The actual codes list is always capped to 20
    - error: reports WKT parsing errors, if any
    - codes: a list of EPSG code objects, each one containg:
        - code: the EPSG code
        - name: the coordinate reference system name
        - url: the full url to the EPSG code description page
    """
    params = dict(mode='wkt', terms=wkt)
    data = urlencode(params)
    data = data.encode('ascii')
    req = urllib2.Request(EPSG_URL, data)
    resp = urllib2.urlopen(req).read()
    result = json.loads(resp.decode())
    return result


def search(text):
    '''Searches epsg.io for a projection name or area of use.
    Functions as a generator that yields each result dictionary.

    NOTE: a new url request has to be made every 10 results, so be careful looping through
    all the results if not necessary.
    
    Each result dict include the following most relevant key entries (for more, see
    https://github.com/maptiler/epsg.io):
    - code
    - name
    - kind
    - bbox
    - wkt
    - proj4
    '''
    link = 'https://epsg.io?' + urlencode({'format':'json', 'q':text})
    # load initial results
    req = urllib2.Request(link, headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
    resp = urllib2.urlopen(req).read()
    result = json.loads(resp.decode())
    # keep loading all pages processed
    page = 1
    i = 0
    while i < result['number_result']:
        # iterate results of current page
        for item in result['results']:
            yield item
            i += 1
        if i < result['number_result']:
            # load next page
            page += 1
            link = 'https://epsg.io?' + urlencode({'format':'json', 'q':text, 'page':page})
            req = urllib2.Request(link,
                                  headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
            resp = urllib2.urlopen(req).read()
            result = json.loads(resp.decode())
            

def search_name(name):
    '''Searches epsg.io for a crs by name.
    Functions as a generator that yields each result dictionary.
    See more details in search() docstring.
    '''
    for item in search('name:'+name):
        yield item


def search_area(area):
    '''Searches epsg.io for a crs by the country or area of use.
    Functions as a generator that yields each result dictionary.
    See more details in search() docstring.
    '''
    for item in search('area:'+area):
        yield item


##def crsstring_to_string(string, newformat):
##    """
##    Search unknown crs string for a match on spatialreference.org.
##    Not very reliable, the search engine does not properly lookup all text.
##    If string is correct there should only be one correct match.
##    Warning: Not finished yet.
##    """
##    link = 'http://spatialreference.org/ref/?search=%s' %string
##    searchresults = urllib2.urlopen(link).read()
##    # pick the first result
##    # ...regex...
##    # go to its url, with extension for the newformat
##    link = 'http://spatialreference.org/ref/%s/%s/%s/' %(codetype,code,newformat)
##    result = urllib2.urlopen(link).read()
##    return result
    



