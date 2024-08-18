class Turtle {
  constructor() {
    this.baseUrl = "https://api.turtle.com";
  }

  async summarise(payload) {
    // make post request to the turtle api.
    const response = await fetch(`${this.baseUrl}/summarise`, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    });
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
