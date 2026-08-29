class RoleControl:

    """
    Role-Based Access Control (RBAC)
    """

    def __init__(self):
        self.roles = {
            "admin": [],
            "trader": [],
            "auditor": []
        }

    def assign_role(self, address: str, role: str):
        if role not in self.roles:
            raise ValueError("Invalid role")

        if address not in self.roles[role]:
            self.roles[role].append(address)

    def revoke_role(self, address: str, role: str):
        if role in self.roles and address in self.roles[role]:
            self.roles[role].remove(address)

    def has_role(self, address: str, role: str):
        return address in self.roles.get(role, [])

    def require_role(self, address: str, role: str):
        if not self.has_role(address, role):
            raise PermissionError("Access denied")

    def list_roles(self, address: str):
        assigned = []
        for role, users in self.roles.items():
            if address in users:
                assigned.append(role)
        return assigned