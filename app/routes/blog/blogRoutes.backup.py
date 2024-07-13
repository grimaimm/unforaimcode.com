# @blogOne_bp.route('/')
# def blogOne():
#     # Mengambil data blog utama dari Firestore
#     blog_ref = db.collection('Blogs').document('1. Exploring the World of Programming')
#     blog_data = blog_ref.get().to_dict()

#     # Meningkatkan jumlah views
#     views_count = blog_data.get('views', 0) + 1 
#     blog_ref.update({'views': views_count})  # Memperbarui nilai views di Firestore

#     # Mengambil koleksi konten blog dari Firestore
#     content_ref = blog_ref.collection('contentBlogOne')
#     blogs = content_ref.stream()

#     blog_contents = []

#     for blog in blogs:
#         blog_dict = blog.to_dict()
#         number = int(blog.id.split('.')[0].strip())  # Mengambil nomor urut dari judul dokumen
#         blog_dict['number'] = number  # Menambahkan nomor urut ke dalam data
#         list_content = blog_dict.get('list', [])  # Mengambil array 'list' dari dokumen
#         html_contents = []

#         for item in list_content:
#             markdown_file_name = item.get('code')
#             if markdown_file_name:
#                 # Baca isi file Markdown
#                 markdown_path = f"app/static/assets/markdown-code/{markdown_file_name}"
#                 with open(markdown_path, 'r') as f:
#                     markdown_content = f.read()
                
#                 # Konversi Markdown ke HTML menggunakan mistune
#                 html_content = mistune.markdown(markdown_content)
#                 item['html_content'] = html_content  # Menambahkan konten HTML ke dalam item

#             html_contents.append(item)

#         blog_dict['list'] = html_contents  # Update list with HTML content
#         blog_contents.append(blog_dict)

#     sorted_blogs = sorted(blog_contents, key=lambda x: x['number'])  # Mengurutkan dokumen berdasarkan nomor urut
#     return render_template('blog-page/blogOne.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs)


# @blogTwo_bp.route('/')
# def blogTwo():
#     # Mengambil data blog utama dari Firestore
#     blog_ref = db.collection('Blogs').document('2. Best Programming Languages to Learn')
#     blog_data = blog_ref.get().to_dict()

#     # Meningkatkan jumlah views
#     views_count = blog_data.get('views', 0) + 1 
#     blog_ref.update({'views': views_count})  # Memperbarui nilai views di Firestore

#     # Mengambil koleksi konten blog dari Firestore
#     content_ref = blog_ref.collection('contentBlogTwo')
#     blogs = content_ref.stream()

#     blog_contents = []

#     for blog in blogs:
#         blog_dict = blog.to_dict()
#         number = int(blog.id.split('.')[0].strip())  # Mengambil nomor urut dari judul dokumen
#         blog_dict['number'] = number  # Menambahkan nomor urut ke dalam data
#         blog_contents.append(blog_dict)

#     sorted_blogs = sorted(blog_contents, key=lambda x: x['number'])  # Mengurutkan dokumen berdasarkan nomor urut
#     return render_template('blog-page/blogTwo.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs)

