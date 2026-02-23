import React from "react";
import {
  Users,
  Calendar,
  Activity,
  TrendingUp,
  Clock,
  ChevronRight,
} from "lucide-react";

const StatCard = ({ icon: Icon, label, value, trend, color }) => (
  <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-start justify-between">
      <div className={`p-3 rounded-xl ${color}`}>
        <Icon className="text-white" size={24} />
      </div>
      {trend && (
        <span className="flex items-center gap-1 text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
          <TrendingUp size={12} />
          {trend}
        </span>
      )}
    </div>
    <div className="mt-4">
      <h3 className="text-gray-400 text-sm font-medium">{label}</h3>
      <p className="text-2xl font-bold mt-1 text-gray-900">{value}</p>
    </div>
  </div>
);

const Dashboard = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Welcome back, here's what's happening today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          label="Total Patients"
          value="1,284"
          trend="+12%"
          color="bg-blue-600"
        />
        <StatCard
          icon={Calendar}
          label="Appointments"
          value="48"
          trend="+4%"
          color="bg-indigo-600"
        />
        <StatCard
          icon={Activity}
          label="Consultations"
          value="32"
          color="bg-violet-600"
        />
        <StatCard
          icon={Clock}
          label="Avg. Wait Time"
          value="14 min"
          trend="-2 min"
          color="bg-sky-600"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Appointments */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold">Upcoming Appointments</h2>
            <button className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1 group">
              View all{" "}
              <ChevronRight
                size={16}
                className="group-hover:translate-x-0.5 transition-transform"
              />
            </button>
          </div>

          <div className="space-y-4">
            {[
              {
                id: 1,
                name: "Sarah Johnson",
                time: "09:30 AM",
                type: "Check-up",
                status: "Confirmed",
              },
              {
                id: 2,
                name: "Michael Chen",
                time: "10:15 AM",
                type: "Follow-up",
                status: "Pending",
              },
              {
                id: 3,
                name: "Amanda Smith",
                time: "11:00 AM",
                type: "Consultation",
                status: "Confirmed",
              },
            ].map((app) => (
              <div
                key={app.id}
                className="flex items-center justify-between p-4 rounded-xl hover:bg-gray-50 transition-colors border border-transparent hover:border-gray-100"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-sm">
                    {app.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">{app.name}</h4>
                    <p className="text-xs text-gray-400">{app.type}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-700">
                    {app.time}
                  </p>
                  <span
                    className={`text-[10px] font-bold uppercase tracking-wider ${
                      app.status === "Confirmed"
                        ? "text-emerald-500"
                        : "text-amber-500"
                    }`}
                  >
                    {app.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions / Stats */}
        <div className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-2xl p-6 text-white shadow-xl shadow-blue-100 relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-lg font-bold mb-2">Clinic Performance</h2>
            <p className="text-indigo-100 text-sm mb-6">
              Your clinic reached its monthly target 4 days early!
            </p>

            <div className="space-y-4">
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-4">
                <p className="text-xs text-indigo-200 mb-1">Weekly Growth</p>
                <p className="text-xl font-bold">24.8%</p>
              </div>
              <button className="w-full py-3 bg-white text-indigo-600 rounded-xl font-bold text-sm hover:bg-indigo-50 transition-colors shadow-lg">
                Download Report
              </button>
            </div>
          </div>

          {/* Decorative element */}
          <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
