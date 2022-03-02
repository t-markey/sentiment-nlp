

 # Bolds keywords in word and sentence column
def bold_keywords(filename):
	with open (filename,'r') as f:
		f_line_list = list(f)
		for i, line in enumerate(f_line_list):

			# Bold and store next line (Word)
			if '<th>' in line: 
				keyword = f_line_list[i+1].strip().replace('<td>','').replace('</td>', '')
				 
				# On first data field set bold
				if keyword in f_line_list[i+1]:
					f_line_list[i+1] = f_line_list[i+1].replace(keyword, '<strong>' +keyword + '</strong>' )
				else:
					pass
				# On last data field for this row, make keyword bold
				if keyword in f_line_list[i+4]:
					f_line_list[i+4] = f_line_list[i+4].replace(keyword, '<strong>' +keyword + '</strong>' )
				else:
					pass


	with open (filename, 'w') as f:
		for line in f_line_list:
			f.write(line)