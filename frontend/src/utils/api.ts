// Call makeRequest, pass in the token
export const makeRequest = (
  path: string,
  token: string
): Promise<Record<string, unknown>> => {
  const url = "http://localhost:8000/api/v1/" + path;

  const headers = new Headers({
    Authorization: `Token ${token}`,
  });

  return fetch(url, {
    method: "GET",
    headers: headers,
  }).then((response) => response.json());
};

export const getToken = (): Promise<{ token: string }> => {
  // define path to get the token
  const url = "http://localhost:8000/api/v1/token-auth";

  // TODO don't hard code the username+password
  const username = "user_one";
  const password = "bad_password";

  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" }, // have to say what format of data  you're sending
    body: JSON.stringify({ username, password }), // this is the data you're sending
  }).then((response) => response.json());
};
