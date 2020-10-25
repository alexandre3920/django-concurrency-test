for i in {1..2}
do
    echo "Requests ($i) begin"
    /Users/alexandre/.virtualenvs/django-doctor-dashboard/bin/python http_create_user_admin_requests.py &
    #sleep 0.1
done
