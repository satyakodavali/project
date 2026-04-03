import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Users, Trash2, PlusCircle } from 'lucide-react';

const AdminDashboard = () => {
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchStudents = async () => {
        try {
            const res = await api.get('/admin/students');
            if (res.data.status === 'success') {
                setStudents(res.data.data);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    const handleDelete = async (roll_no) => {
        if (!window.confirm(`Are you sure you want to delete student ${roll_no}?`)) return;

        try {
            const res = await api.delete(`/admin/student/${roll_no}`);
            if (res.data.status === 'success') {
                fetchStudents();
            }
        } catch (err) {
            alert('Error deleting student');
        }
    };

    return (
        <div style={{ padding: '2.5rem', background: '#f8fafc', minHeight: 'calc(100vh - 72px)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', margin: 0 }}>
                        <Users size={32} color="var(--primary-color)" /> Admin Dashboard
                    </h1>
                    <p style={{ color: 'var(--text-light)', marginTop: '0.5rem' }}>Manage users, view statistics, and update records.</p>
                </div>

                <button className="btn btn-primary" onClick={() => alert("Open Add Student Form Modal - Feature in development")}>
                    <PlusCircle size={18} /> Add New Student
                </button>
            </div>

            <div className="card">
                <h2 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>Student Directory</h2>

                {loading ? (
                    <p>Loading records...</p>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Roll No</th>
                                    <th>Name</th>
                                    <th>Branch</th>
                                    <th>Section</th>
                                    <th>Year</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {students.map((student) => (
                                    <tr key={student.roll_no}>
                                        <td style={{ fontWeight: 600 }}>{student.roll_no}</td>
                                        <td>{student.name}</td>
                                        <td>{student.branch}</td>
                                        <td>{student.section}</td>
                                        <td>{student.year}</td>
                                        <td>
                                            <button
                                                onClick={() => handleDelete(student.roll_no)}
                                                style={{ background: 'var(--danger)', color: 'white', border: 'none', padding: '0.5rem', borderRadius: '0.25rem', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                                                title="Delete Student"
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {students.length === 0 && (
                                    <tr>
                                        <td colSpan="6" style={{ textAlign: 'center', padding: '2rem' }}>No student records found.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;
