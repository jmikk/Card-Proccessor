#!/usr/bin/env python3
import re
import os

with open('junk_list.txt') as f:
    junk = f.read().split('\n')
with open('sell_list.txt') as h:
    sellables = h.read().split('\n')

junkables = list(filter(None, junk))

#chunk size adjustable, 5000 is low latency for me
chunk_size = 5000
num_chunks = len(junkables) // chunk_size + 1
for chunk_num in range(num_chunks):
    start_idx = chunk_num * chunk_size
    end_idx = min((chunk_num + 1) * chunk_size, len(junkables))
    
    html_filename = f'junkable_{start_idx}-{end_idx}.html'
    with open(html_filename, 'w') as links:
        links.write("""
        <html>
        <head>
        <style>
        td.createcol p {
            padding-left: 10em;
        }
        
        a {
            text-decoration: none;
            color: black;
        }
        
        a:visited {
            color: grey;
        }
        
        table {
            border-collapse: collapse;
            display: table-cell;
            max-width: 100%;
            border: 1px solid darkorange;
        }
        
        tr, td {
            border-bottom: 1px solid darkorange;
        }
        
        td p {
            padding: 0.5em;
        }
        
        tr:hover {
            background-color: lightgrey;
        }
        
        </style>
        </head>
        <body>
        <table>
        """)

        chunk_junkables = junkables[start_idx:end_idx]
        totalcount = len(junkables)

        for idx, k in enumerate(chunk_junkables, start=start_idx + 1):
            canonical = k.lower().replace(" ", "_")
            escaped_canonical = re.escape(canonical)
            links.write("""<tr>""")
            links.write("""<td>{} of {}</td>""".format(idx, totalcount))
            links.write("""<td><p><a target="_blank" href="{}">Link to Junk</a></p></td>""".format(canonical, canonical, canonical))
            links.write("""</tr>\n""")
        
        links.write("""
        <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>
        <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""".format(canonical))
        links.write("""
        </table>
        <script>
        document.querySelectorAll("td").forEach(function(el) {
            el.addEventListener("click", function() {
                let myidx = 0;
                const row = el.parentNode;
                let child = el;
                while((child = child.previousElementSibling) != null) {
                    myidx++;
                }
                row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
                row.parentNode.removeChild(row);
            });
        });
        </script>
        </body>
        """)

sellables_html_filename = 'sellables.html'
with open(sellables_html_filename, 'w') as sellables_links:
    sellables_links.write("""
    <html>
    <head>
    <style>
    td.createcol p {
        padding-left: 10em;
    }
    
    a {
        text-decoration: none;
        color: black;
    }
    
    a:visited {
        color: grey;
    }
    
    table {
        border-collapse: collapse;
        display: table-cell;
        max-width: 100%;
        border: 1px solid darkorange;
    }
    
    tr, td {
        border-bottom: 1px solid darkorange;
    }
    
    td p {
        padding: 0.5em;
    }
    
    tr:hover {
        background-color: lightgrey;
    }
    
    </style>
    </head>
    <body>
    <table>
    """)

    for idx, k in enumerate(sellables):
        each = k.lower().replace(" ", "_")
        sellables_links.write("""<tr>""")
        sellables_links.write("""<td>{} of {}</td>""".format(idx + 1, len(sellables)))
        sellables_links.write(f'<td><p><a target="_blank" href="{each}">Link to Gift</a></p></td>')
        sellables_links.write("""</tr>\n""")
    
    sellables_links.write("""
    <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>
    <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""")
    sellables_links.write("""
    </table>
    <script>
    document.querySelectorAll("td").forEach(function(el) {
        el.addEventListener("click", function() {
            let myidx = 0;
            const row = el.parentNode;
            let child = el;
            while((child = child.previousElementSibling) != null) {
                myidx++;
            }
            row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
            row.parentNode.removeChild(row);
        });
    });
    </script>
    </body>
    """)

print("HTML files generated successfully.")
