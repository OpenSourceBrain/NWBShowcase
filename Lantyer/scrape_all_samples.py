import requests
import lxml.html as lh
import pandas as pd
import re

# set number of table pages with different URLs
MAX_PAGES = 33

def get_reduced_split(metadata,headers):

    # hard encoding of split
    headers = ['Age','Description','Life stage','Sex','Collection date']
    delimiters = [head+':' for head in headers] + ['+','...','\t\t','\n']
    regexPattern = '|'.join(map(re.escape, delimiters))

    split = re.split(regexPattern,metadata)
    split = [o for o in split if not o.isspace()] # remove whitespace
    split = [o for o in split if len(o)>0][3:] # remove empty strings + first 3 are redudant

    reduced_split = []

    for i, s in enumerate(split):

        if i ==1:
            reduced_split.append(split[1] + ' ' + split[2])
        elif i==2:
            continue
        else:
            reduced_split.append(s)

    return reduced_split



if __name__ == '__main__':

    for page_i in range(MAX_PAGES):

        if page_i == 0:
            url = 'http://gigadb.org/dataset/view/id/100535' # page 1
        else:
            url = 'http://gigadb.org/dataset/view/id/100535/Sample_page/'+str(page_i+1)

        # get table elements from webpage
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')

        # take the first 11 rows -> table rows for samples
        max_size = len(tr_elements[0])
        header_elements = tr_elements[0]
        sample_elements = tr_elements[1:11]


        # column labels for DataFrame
        columns = []

        for i,h in enumerate(header_elements):
            name = h.text_content()

            if i == max_size-1:
                break

            columns.append((name,[]))

        # replace final column with specific column headers
        nwb_col_headers = ['Description','Age','Sex','Collection date']
        for h in nwb_col_headers:
            columns.append((h,[]))




        # fill in metadata
        for i, sample in enumerate(sample_elements):
            if len(sample)!=max_size:
                print('Sample %s (length %s) on page %s is not of size %s'%(i+1,len(sample),page_i+1,max_size))
                break # should be final one if any

            for j,s in enumerate(sample.iterchildren()):
                metadata = s.text_content()

                # split "Sample attributes"
                if j==max_size-1:
                    # get split data
                    split = get_reduced_split(metadata,nwb_col_headers)

                    for k in range(len(nwb_col_headers)):
                        columns[max_size-1+k][1].append(split[k])

                else:
                    columns[j][1].append(metadata)




        # create dataframe
        Dict = {title:col for (title,col) in columns}

        if page_i == 0:
            samples_df = pd.DataFrame(Dict)
        else:
            temp_df = pd.DataFrame(Dict)

            join_frames = [samples_df,temp_df]
            samples_df = pd.concat(join_frames,ignore_index=True)

    # save file
    samples_df.to_pickle('sample_metadata.pkl')
