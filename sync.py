#!/usr/bin/env python

import re, argparse, sqlite3, subprocess

def main():
    
    parser = argparse.ArgumentParser(description='Include a local man page in the Unix/Linux Android Man Page App')
    parser.add_argument('-f', '--file', help="path to manpages sqlite file on the device SD card")
    parser.add_argument('-m', '--man', help="man pages to add, comma separated")
    parser.add_argument('-u', '--update', help="allow update of pages")
    args = parser.parse_args();
    
    if (not args.file):
        print "--file is required, -h to see options"
        exit(1)

    if (not args.man):
        print "--man (manpage) is required"
        exit(1)
    
    
    conn = sqlite3.connect(args.file)
    c = conn.cursor()
    try:
        c.execute("SELECT name FROM manpage LIMIT 1")
        for row in c:
            print "sample row found"
            print row[0]
    except:
        print "database not recognized.  manpage table should exist"
        exit(2)

    manpages = args.man.split(',')
    for (mp) in manpages:
        page = man_to_string(mp)
        lines = page.split('\n')
        m = re.search('([a-zA-Z0-9_()]+)', lines[0])
        if (not m):
            m = re.search('([a-zA-Z0-9_()]+)', lines[1])
            
        if (m and m.group(1)):
            command = m.group(1).lower().strip()
            print command
            name = ''
            next_name = 0
            for line in lines:
                if (re.search('NAME', line)):
                    next_name = 1
                elif next_name and not name:
                    name = line.strip()
                    break
            
            if (not name):
                print "name could not be determined, skip"
            else:
                print 'find: "' + command  +'" - "' + name + '"'
                c.execute("SELECT name FROM manpage WHERE lower(command) = ?", (command,))
                found = 0
                for row in c:
                    found = 1
                if found:
                    print "command found: " + row[0]
                    if (args.update):
                        c.execute("UPDATE manpage SET name = ?, description = ? WHERE command = ?", (name, page, command,))
                    else:
                        print "pass --update to enable update (todo)"
                else:
                    print "not found, inserting"
                    c.execute("INSERT INTO manpage (command, name, description) VALUES (?,?,?)", (command,name,page,))
                #found?
            #name?
        #parseable?
    #each manpage 

    conn.commit()
    c.close()
    
def man_to_string(page): 
    return subprocess.check_output("man -P cat " + page + ' | col -b ', shell=True)

if __name__ == "__main__":
    main()
