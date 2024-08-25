import config from "../constants/config.js";
class Turtle {
  constructor() {
    this.version = config.TURTLE_API_VERSION;
    this.baseUrl = `${config.TURTLE_API}/api/${this.version}`;
  }

  async summerize(diff) {
    const file_diff = {
      file_diff: JSON.stringify(diff),
    };
    console.log(JSON.stringify(file_diff));
    const response = await fetch(`${this.baseUrl}/summarize`, {
      method: "POST",
      body: JSON.stringify(file_diff),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log(response);
    return response.json();
  }

  async review() {
    // make post request to the turtle api.
    const response = await fetch(`${this.baseUrl}/review`, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.json();
  }
}

const turtle = new Turtle();
export { turtle };
