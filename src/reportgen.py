import json
import urllib2
import ho.pisa as pisa 
import argparse
import logging
class PisaLogHandler(logging.Handler):
    def emit(self, record):
        print record
        
logging.getLogger("ho.pisa").addHandler(PisaLogHandler())

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

def printPdf(text,openPdf,filename):

    text = wrap(text, 100)
    
    print "Writing to PDF file: " + filename
    f = file(filename, "wb")
    pdf = pisa.CreatePDF(text, f)
    
    if openPdf:
        if not pdf.err:                           
            pisa.startViewer(filename)   
        f.close()
        
    print "Writing to PDF file DONE!"
    
def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        unencoded_string = str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        unencoded_string = unicode(obj)

    return unencoded_string.encode('utf8')

def get_issue_comments(user,repos,issue_number):
    print "Getting comments for issue: " + issue_number
     
    request = urllib2.Request("https://api.github.com/repos/"+user+"/"+repos+"/issues/"+issue_number+"/comments", headers={"Accept" : "application/vnd.github.beta.html+json"})
    json_data = urllib2.urlopen(request).read()

    data = json.loads(json_data)
    
    if(len(data) > 0):
        return data[0]['body_html']
    else:
        return ""
    
def create_report(user,repos,openPdf,output_file):
    printPdf( safe_str( "<html><body>" + get_all_issues("1",user,repos) + "</body></html>" ), openPdf, output_file )
    
def get_all_issues(page, user, repos):
     
    request = urllib2.Request("https://api.github.com/repos/"+user+"/"+repos+"/issues?page="+page, headers={"Accept" : "application/vnd.github.beta.html+json"})
    response = urllib2.urlopen(request)
    json_data = response.read()

    issues = json.loads(json_data)
    
    if(len(issues) == 0):
        #recursion stop case
        
        print "Getting issues DONE!"
        
        return ""
    else:
        print "Getting issues page: " + page
  
        pdfText = ""
        
        for issue in issues:
            pdfText += "<h1>"+ issue['title'] + "</h1>"
            pdfText += get_issue_comments( user, repos, str(issue['number']) )
        
        return pdfText + get_all_issues( str( int(page) + 1), user, repos )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='github username', required=True)
    parser.add_argument('-r', '--repos', help='github repository name', required=True)
    parser.add_argument('--open', help='when set, open the resulting PDF automatically', action='store_true')
    parser.add_argument('-o', '--out', help='file output name ( defaults to {user}-report.pdf )', required=False)
    args = parser.parse_args()

    user = args.user
    repos = args.repos
    openPdf = args.open
    
    out = args.out
    if(out is None):
        out = user + "-report.pdf"

    create_report(user,repos,openPdf,out)
        