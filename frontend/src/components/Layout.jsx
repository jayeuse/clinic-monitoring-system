import React from "react";
import {
  LayoutDashboard,
  Users,
  Calendar,
  Settings,
  LogOut,
  Search,
  Bell,
  User,
} from "lucide-react";

const SidebarItem = ({ icon: Icon, label, active = false }) => (
  <div
    className={`flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer transition-all duration-200 ${
      active
        ? "bg-blue-600 text-white shadow-lg shadow-blue-200"
        : "text-gray-500 hover:bg-blue-50 hover:text-blue-600"
    }`}
  >
    <Icon size={20} />
    <span className="font-medium">{label}</span>
  </div>
);

const Layout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-100 flex flex-col p-6 fixed h-full">
        <div className="flex items-center gap-2 mb-10 px-2">
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-200">
            <span className="font-bold text-xl">C</span>
          </div>
          <span className="font-bold text-xl tracking-tight">
            Clinic<span className="text-blue-600">Sync</span>
          </span>
        </div>

        <nav className="flex-1 space-y-2">
          <SidebarItem icon={LayoutDashboard} label="Dashboard" active />
          <SidebarItem icon={Users} label="Patients" />
          <SidebarItem icon={Calendar} label="Appointments" />
          <SidebarItem icon={Settings} label="Settings" />
        </nav>

        <div className="mt-auto border-t border-gray-100 pt-6">
          <SidebarItem icon={LogOut} label="Logout" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64">
        {/* Header */}
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 px-8 flex items-center justify-between sticky top-0 z-10">
          <div className="relative w-96">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
              size={18}
            />
            <input
              type="text"
              placeholder="Search anything..."
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-100 transition-all outline-none text-sm"
            />
          </div>

          <div className="flex items-center gap-4">
            <button className="p-2.5 text-gray-500 hover:bg-gray-50 rounded-xl transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
            </button>
            <div className="h-8 w-[1px] bg-gray-100 mx-2"></div>
            <div className="flex items-center gap-3 pl-2">
              <div className="text-right">
                <p className="text-sm font-semibold">Dr. Smith</p>
                <p className="text-xs text-gray-400 uppercase tracking-wider font-medium">
                  Administrator
                </p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-500 rounded-xl flex items-center justify-center text-white shadow-md shadow-blue-100 cursor-pointer overflow-hidden">
                <User size={20} />
              </div>
            </div>
          </div>
        </header>

        {/* Page Area */}
        <div className="p-8 max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
};

export default Layout;
