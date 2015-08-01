import urllib2
import re

def build_crs_table(savepath):
    """
    Build crs table of all equivalent format variations by scraping spatialreference.org.
    Takes a while.
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
                link = 'http://spatialreference.org/ref/%s/?page=%s' %(codetype,page)
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
            link = 'http://spatialreference.org/ref/%s/%s/' %(codetype,code)
            urllib2.urlopen(link)
            
            # collect each projection format in a table row
            row = [codetype, code]
            for resulttype in ("proj4", "ogcwkt", "esriwkt"):
                try:
                    link = 'http://spatialreference.org/ref/%s/%s/%s/' %(codetype,code,resulttype)
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
    Lookup crscode on spatialreference.org and return in specified format.

    - codetype: "epsg", "esri", or "sr-org"
    - code: The code
    - format: The crs format of the returned string. One of "ogcwkt", "esriwkt", or "proj4", but also several others...
    """
    link = 'http://spatialreference.org/ref/%s/%s/%s/' %(codetype,code,format)
    result = urllib2.urlopen(link).read()
    return result

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
    

##if __name__ == "__main__":
##    build_crs_table("crstable.txt")


