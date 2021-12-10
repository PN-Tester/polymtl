This is a tool I developed quickly, which allows users to visualize class availability by day of the week for a given program at polymtl.
The schedule building tools available on dossier-etudiant are not currently capable of doing this.
There is also currently no way to filter on a per-day basis when checking for classes using the polymtl.ca website.
This tool circumvents this issue by automatically acquiring all the classes for a given program and allowing you to filter based on day of the week.
Only courses offered in the next semester open for registration will be shown. This ensures only valid results are displayed to the user when querying a day.

This tool works for ANY program offered at polymtl, not just cybersecurity related programs hardcoded in the menu. 
If you want to load a different program, use the "OTHER" option from the main menu to specify the program URL. 
For example, to acquire class information for the cyberinvestigation microprogram which is not included in the main menu, you would input the following URL when prompted : https://www.polymtl.ca/programmes/programmes/microprogramme-de-1er-cycle-en-cyberinvestigation

NOTE that this was developped quickly, for personal use only. It was never my intention to make this publicly available, but due to increased interest in schedule
building solutions mentioned in the forum, I have decided to post it here.

This wont be maintained! Feel free to modify it. 
Enjoy!

INSTALLATION :

1) git clone https://github.com/PN-Tester/polymtl
2) cd polymtl
3) pip3 install -r requirements.txt 
4) python3 polyScrape.py 

INSTALL + USAGE :
<img src="https://raw.githubusercontent.com/PN-Tester/polymtl/main/recording.svg">
