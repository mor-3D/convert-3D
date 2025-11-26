# convert-3D
📦 פרויקט המרה לתלת־ממד (3D Reconstruction System)

מערכת מלאה להמרת סדרת תמונות למודל תלת־ממד בפורמט PLY, הכוללת:

צד שרת (Backend) בפייתון

צד לקוח (Frontend) ב־React

אלגוריתמיקה של Structure from Motion (SfM)

יצירת Point Cloud ו־Mesh באמצעות OpenCV + Open3D

ממשק משתמש להעלאת תמונות וצפייה במודל תלת־ממד

🧠 תיאור כללי

המערכת מאפשרת למשתמש להעלות מספר תמונות של אובייקט מכל מיני זוויות →
השרת מריץ תהליך רקונסטרוקציה תלת־ממדית הכולל:

גילוי נקודות מעניינות (SIFT)

התאמת תכונות בין תמונות

חישוב מטריצת Essential והערכת תנוחה (R, t)

טריאנגולציה ליצירת נקודות תלת־ממד

יצירת point cloud

בניית mesh בשיטת Poisson Reconstruction

צביעת המודל לפי המידע מהתמונות

שליחה ללקוח להורדה / הצגה

🛠 טכנולוגיות
✔ צד שרת (Backend)

Python

Flask

OpenCV

Open3D

NumPy

PIL

SQLite (רישום והתחברות משתמשים)

✔ צד לקוח (Frontend)

React

JavaScript

CSS

Three.js

PLYLoader (להצגת מודלים תלת־ממדיים)

📁 מבנה הפרויקט – צד שרת (Backend)
main.py 

main

מנוע הרקונסטרוקציה התלת־ממדית:

טעינת תמונות

זיהוי נקודות (SIFT)

התאמת נקודות

טריאנגולציה

יצירת point cloud

יצירת mesh בשיטת Poisson Reconstruction

צביעת המודל

שמירה לקובץ .ply

SFM.py 

SFM

מימוש Algorithm של Structure from Motion:

זיהוי תכונות והתאמתן בין תמונות

חישוב מטריצות Essential

התאמת תנוחות מצלמה

טריאנגולציה ל־3D

point_cloude.py 

point_cloude

ניהול point cloud:

חישוב נורמלים

Poisson Reconstruction

סינון נקודות לפי צפיפות

צביעת משולשים

שמירה וויזואליזציה

cut_object.py 

cut_object

מחיקת רקע מתמונות לדיוק גבוה יותר.

server.py 

server

API צד שרת:

רישום / התחברות משתמשים

העלאת תמונות לשרת

הרצת בניית המודל

שליחת קובץ ה־PLY ללקוח

📁 מבנה הפרויקט – צד לקוח (Frontend)
buttons.js 

buttons

לולאת העלאת התמונות + שליחתן לשרת וביצוע ההורדה.

model3D.js 

model3D

מציג את המודל התלת־ממדי באמצעות:

Three.js

PLYLoader

תאורה, מצלמה, סיבוב אוטומטי ועוד

login.js / signIn.js

מערכת התחברות ורישום.

picToServer.js 

picToServer

מנהל העלאת תמונה בודדת (גרסה מוקדמת).

style.css / components.css

עיצוב למערכת.

🧰 תהליך העבודה (Workflow)

המשתמש מעלה סדרת תמונות מהדפדפן.

התמונות נשלחות לשרת דרך /upload.

השרת מריץ את אלגוריתם ה־SfM:
✔ התאמת מאפיינים
✔ טריאנגולציה
✔ בניית point cloud

השרת בונה mesh תלת־ממדי.

המודל נשמר כ־PLY.

המודל נשלח ללקוח:

להורדה

להצגה באמצעות Three.js

▶️ הפעלה
צד שרת:
cd server
python server.py

צד לקוח:
cd client
npm install
npm start
