from flask import Flask, render_template
import pandas as pd

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/")
def dashboard():

    try:
        df = pd.read_csv("reports/alerts.csv")

        total_alerts = len(df)

        dns_attacks = len(df[df["protocol"] == "DNS"])
        arp_attacks = len(df[df["protocol"] == "ARP"])


        recent_alerts = (
            df.tail(20)
            .sort_index(ascending=False)
            .to_dict(orient="records")
        )

    except Exception:
        total_alerts = 0
        dns_attacks = 0
        arp_attacks = 0
        recent_alerts = []


    return render_template(
        "dashboard.html",
        total_alerts=total_alerts,
        dns_attacks=dns_attacks,
        arp_attacks=arp_attacks,
        recent_alerts=recent_alerts
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
