-- ============================================
-- BANGLADESH HEALTHCARE DATABASE SAMPLE DATA
-- ============================================

-- ------------------------------
-- Lookup Tables
-- ------------------------------

-- Roles
INSERT INTO roles (role_id, role_name) VALUES
(1, 'Patient'),
(2, 'Doctor'),
(3, 'Admin'),
(4, 'Super Admin'),
(5, 'Support Staff'),
(6, 'Pharmacist'),
(7, 'Lab Technician'),
(8, 'Receptionist'),
(9, 'Nurse'),
(10, 'Medical Assistant');

-- Genders
INSERT INTO genders (gender_id, gender_name) VALUES
(1, 'Male'),
(2, 'Female'),
(3, 'Other'),
(4, 'Prefer not to say');

-- Appointment Status
INSERT INTO appointment_status (status_id, status_name) VALUES
(1, 'Scheduled'),
(2, 'Confirmed'),
(3, 'Completed'),
(4, 'Cancelled'),
(5, 'Rescheduled'),
(6, 'No Show'),
(7, 'In Progress'),
(8, 'Waiting'),
(9, 'Rejected'),
(10, 'Pending');

-- Reminder Types
INSERT INTO reminder_types (reminder_type_id, type_name) VALUES
(1, 'SMS'),
(2, 'Email'),
(3, 'Push Notification'),
(4, 'WhatsApp'),
(5, 'Phone Call'),
(6, 'In-App'),
(7, 'Telegram'),
(8, 'Facebook Messenger'),
(9, 'Voice Call'),
(10, 'Auto Dialer');

-- Reminder Status
INSERT INTO reminder_status (reminder_status_id, status_name) VALUES
(1, 'Pending'),
(2, 'Sent'),
(3, 'Delivered'),
(4, 'Failed'),
(5, 'Read'),
(6, 'Scheduled'),
(7, 'Cancelled'),
(8, 'Retry'),
(9, 'Expired'),
(10, 'Acknowledged');

-- Payment Methods
INSERT INTO payment_methods (method_id, method_name) VALUES
(1, 'bKash'),
(2, 'Nagad'),
(3, 'Rocket'),
(4, 'Cash'),
(5, 'Credit Card'),
(6, 'Debit Card'),
(7, 'Bank Transfer'),
(8, 'Upay'),
(9, 'SureCash'),
(10, 'PayPal');

-- Payment Status
INSERT INTO payment_status (status_id, status_name) VALUES
(1, 'Pending'),
(2, 'Completed'),
(3, 'Failed'),
(4, 'Refunded'),
(5, 'Cancelled'),
(6, 'Processing'),
(7, 'On Hold'),
(8, 'Disputed'),
(9, 'Partially Paid'),
(10, 'Verified');

-- Blood Groups
INSERT INTO blood_group (blood_group_id, blood_group_name) VALUES
(1, 'A+'),
(2, 'A-'),
(3, 'B+'),
(4, 'B-'),
(5, 'O+'),
(6, 'O-'),
(7, 'AB+'),
(8, 'AB-'),
(9, 'Unknown'),
(10, 'Not Tested');


-- ============================================
-- BANGLADESH ADMINISTRATIVE DIVISIONS
-- Complete Database Insert Statements
-- ============================================

-- ============================================
-- DIVISIONS (8 Total)
-- ============================================
INSERT INTO divisions (division_id, division_name) VALUES
(1, 'Dhaka'),
(2, 'Chattogram'),
(3, 'Rajshahi'),
(4, 'Khulna'),
(5, 'Barishal'),
(6, 'Sylhet'),
(7, 'Rangpur'),
(8, 'Mymensingh');

-- ============================================
-- DISTRICTS (64 Total)
-- ============================================

-- Dhaka Division (13 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(1, 'Dhaka', 1),
(2, 'Faridpur', 1),
(3, 'Gazipur', 1),
(4, 'Gopalganj', 1),
(5, 'Kishoreganj', 1),
(6, 'Madaripur', 1),
(7, 'Manikganj', 1),
(8, 'Munshiganj', 1),
(9, 'Narayanganj', 1),
(10, 'Narsingdi', 1),
(11, 'Rajbari', 1),
(12, 'Shariatpur', 1),
(13, 'Tangail', 1);

-- Chattogram Division (11 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(14, 'Bandarban', 2),
(15, 'Brahmanbaria', 2),
(16, 'Chandpur', 2),
(17, 'Chattogram', 2),
(18, 'Comilla', 2),
(19, 'Coxs Bazar', 2),
(20, 'Feni', 2),
(21, 'Khagrachari', 2),
(22, 'Lakshmipur', 2),
(23, 'Noakhali', 2),
(24, 'Rangamati', 2);

-- Rajshahi Division (8 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(25, 'Bogura', 3),
(26, 'Joypurhat', 3),
(27, 'Naogaon', 3),
(28, 'Natore', 3),
(29, 'Chapainawabganj', 3),
(30, 'Pabna', 3),
(31, 'Rajshahi', 3),
(32, 'Sirajganj', 3);

-- Khulna Division (10 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(33, 'Bagerhat', 4),
(34, 'Chuadanga', 4),
(35, 'Jessore', 4),
(36, 'Jhenaidah', 4),
(37, 'Khulna', 4),
(38, 'Kushtia', 4),
(39, 'Magura', 4),
(40, 'Meherpur', 4),
(41, 'Narail', 4),
(42, 'Satkhira', 4);

-- Barishal Division (6 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(43, 'Barguna', 5),
(44, 'Barishal', 5),
(45, 'Bhola', 5),
(46, 'Jhalokati', 5),
(47, 'Patuakhali', 5),
(48, 'Pirojpur', 5);

-- Sylhet Division (4 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(49, 'Habiganj', 6),
(50, 'Moulvibazar', 6),
(51, 'Sunamganj', 6),
(52, 'Sylhet', 6);

-- Rangpur Division (8 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(53, 'Dinajpur', 7),
(54, 'Gaibandha', 7),
(55, 'Kurigram', 7),
(56, 'Lalmonirhat', 7),
(57, 'Nilphamari', 7),
(58, 'Panchagarh', 7),
(59, 'Rangpur', 7),
(60, 'Thakurgaon', 7);

-- Mymensingh Division (4 districts)
INSERT INTO districts (district_id, district_name, division_id) VALUES
(61, 'Jamalpur', 8),
(62, 'Mymensingh', 8),
(63, 'Netrokona', 8),
(64, 'Sherpur', 8);

-- ============================================
-- UPAZILAS (492 Total)
-- ============================================

-- Dhaka District (47 upazilas including thanas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(1, 'Adabor', 1),
(2, 'Badda', 1),
(3, 'Banani', 1),
(4, 'Bangshal', 1),
(5, 'Biman Bandar', 1),
(6, 'Cantonment', 1),
(7, 'Chak Bazar', 1),
(8, 'Dakshinkhan', 1),
(9, 'Darus Salam', 1),
(10, 'Demra', 1),
(11, 'Dhanmondi', 1),
(12, 'Dohar', 1),
(13, 'Gendaria', 1),
(14, 'Gulshan', 1),
(15, 'Hazaribagh', 1),
(16, 'Jatrabari', 1),
(17, 'Kadamtali', 1),
(18, 'Kafrul', 1),
(19, 'Kalabagan', 1),
(20, 'Kamrangir Char', 1),
(21, 'Keraniganj', 1),
(22, 'Khilgaon', 1),
(23, 'Khilkhet', 1),
(24, 'Kotwali', 1),
(25, 'Lalbagh', 1),
(26, 'Mirpur', 1),
(27, 'Mohammadpur', 1),
(28, 'Motijheel', 1),
(29, 'Nawabganj', 1),
(30, 'New Market', 1),
(31, 'Pallabi', 1),
(32, 'Paltan', 1),
(33, 'Ramna', 1),
(34, 'Rampura', 1),
(35, 'Sabujbagh', 1),
(36, 'Savar', 1),
(37, 'Shah Ali', 1),
(38, 'Shahbagh', 1),
(39, 'Shahjahanpur', 1),
(40, 'Sher-e-Bangla Nagar', 1),
(41, 'Shyampur', 1),
(42, 'Sutrapur', 1),
(43, 'Tejgaon', 1),
(44, 'Tejgaon Industrial Area', 1),
(45, 'Turag', 1),
(46, 'Uttara', 1),
(47, 'Uttarkhan', 1);

-- Faridpur District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(48, 'Alfadanga', 2),
(49, 'Bhanga', 2),
(50, 'Boalmari', 2),
(51, 'Char Bhadrasan', 2),
(52, 'Faridpur Sadar', 2),
(53, 'Madhukhali', 2),
(54, 'Nagarkanda', 2),
(55, 'Sadarpur', 2),
(56, 'Saltha', 2);

-- Gazipur District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(57, 'Gazipur Sadar', 3),
(58, 'Kaliakair', 3),
(59, 'Kaliganj', 3),
(60, 'Kapasia', 3),
(61, 'Sreepur', 3);

-- Gopalganj District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(62, 'Gopalganj Sadar', 4),
(63, 'Kashiani', 4),
(64, 'Kotalipara', 4),
(65, 'Muksudpur', 4),
(66, 'Tungipara', 4);

-- Kishoreganj District (13 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(67, 'Astagram', 5),
(68, 'Bajitpur', 5),
(69, 'Bhairab', 5),
(70, 'Hossainpur', 5),
(71, 'Itna', 5),
(72, 'Karimganj', 5),
(73, 'Katiadi', 5),
(74, 'Kishoreganj Sadar', 5),
(75, 'Kuliarchar', 5),
(76, 'Mithamain', 5),
(77, 'Nikli', 5),
(78, 'Pakundia', 5),
(79, 'Tarail', 5);

-- Madaripur District (4 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(80, 'Madaripur Sadar', 6),
(81, 'Kalkini', 6),
(82, 'Rajoir', 6),
(83, 'Shibchar', 6);

-- Manikganj District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(84, 'Daulatpur', 7),
(85, 'Ghior', 7),
(86, 'Harirampur', 7),
(87, 'Manikganj Sadar', 7),
(88, 'Saturia', 7),
(89, 'Shivalaya', 7),
(90, 'Singair', 7);

-- Munshiganj District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(91, 'Gazaria', 8),
(92, 'Lohajang', 8),
(93, 'Munshiganj Sadar', 8),
(94, 'Sirajdikhan', 8),
(95, 'Sreenagar', 8),
(96, 'Tongibari', 8);

-- Narayanganj District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(97, 'Araihazar', 9),
(98, 'Bandar', 9),
(99, 'Narayanganj Sadar', 9),
(100, 'Rupganj', 9),
(101, 'Sonargaon', 9),
(102, 'Siddhirganj', 9);

-- Narsingdi District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(103, 'Belabo', 10),
(104, 'Monohardi', 10),
(105, 'Narsingdi Sadar', 10),
(106, 'Palash', 10),
(107, 'Raipura', 10),
(108, 'Shibpur', 10);

-- Rajbari District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(109, 'Baliakandi', 11),
(110, 'Goalandaghat', 11),
(111, 'Pangsha', 11),
(112, 'Rajbari Sadar', 11),
(113, 'Kalukhali', 11);

-- Shariatpur District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(114, 'Bhedarganj', 12),
(115, 'Damudya', 12),
(116, 'Gosairhat', 12),
(117, 'Naria', 12),
(118, 'Shariatpur Sadar', 12),
(119, 'Zajira', 12),
(120, 'Shakhipur', 12);

-- Tangail District (12 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(121, 'Basail', 13),
(122, 'Bhuapur', 13),
(123, 'Delduar', 13),
(124, 'Dhanbari', 13),
(125, 'Ghatail', 13),
(126, 'Gopalpur', 13),
(127, 'Kalihati', 13),
(128, 'Madhupur', 13),
(129, 'Mirzapur', 13),
(130, 'Nagarpur', 13),
(131, 'Sakhipur', 13),
(132, 'Tangail Sadar', 13);

-- Bandarban District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(133, 'Alikadam', 14),
(134, 'Bandarban Sadar', 14),
(135, 'Lama', 14),
(136, 'Naikhongchhari', 14),
(137, 'Rowangchhari', 14),
(138, 'Ruma', 14),
(139, 'Thanchi', 14);

-- Brahmanbaria District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(140, 'Akhaura', 15),
(141, 'Bancharampur', 15),
(142, 'Brahmanbaria Sadar', 15),
(143, 'Ashuganj', 15),
(144, 'Kasba', 15),
(145, 'Nabinagar', 15),
(146, 'Nasirnagar', 15),
(147, 'Sarail', 15),
(148, 'Bijoynagar', 15);

-- Chandpur District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(149, 'Chandpur Sadar', 16),
(150, 'Faridganj', 16),
(151, 'Haimchar', 16),
(152, 'Haziganj', 16),
(153, 'Kachua', 16),
(154, 'Matlab Dakshin', 16),
(155, 'Matlab Uttar', 16),
(156, 'Shahrasti', 16);

-- Chattogram District (22 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(157, 'Anwara', 17),
(158, 'Banshkhali', 17),
(159, 'Boalkhali', 17),
(160, 'Chandanaish', 17),
(161, 'Chattogram Sadar', 17),
(162, 'Fatikchhari', 17),
(163, 'Hathazari', 17),
(164, 'Karnaphuli', 17),
(165, 'Lohagara', 17),
(166, 'Mirsharai', 17),
(167, 'Patiya', 17),
(168, 'Rangunia', 17),
(169, 'Raozan', 17),
(170, 'Sandwip', 17),
(171, 'Satkania', 17),
(172, 'Sitakunda', 17),
(173, 'Akbar Shah', 17),
(174, 'Bakalia', 17),
(175, 'Bandar', 17),
(176, 'Bayazid Bostami', 17),
(177, 'Chawk Bazar', 17),
(178, 'Double Mooring', 17);

-- Comilla District (17 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(179, 'Barura', 18),
(180, 'Brahmanpara', 18),
(181, 'Burichang', 18),
(182, 'Chandina', 18),
(183, 'Chauddagram', 18),
(184, 'Comilla Sadar', 18),
(185, 'Daudkandi', 18),
(186, 'Debidwar', 18),
(187, 'Homna', 18),
(188, 'Laksam', 18),
(189, 'Meghna', 18),
(190, 'Muradnagar', 18),
(191, 'Nangalkot', 18),
(192, 'Comilla Sadar South', 18),
(193, 'Titas', 18),
(194, 'Monohargonj', 18),
(195, 'Lalmai', 18);

-- Coxs Bazar District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(196, 'Chakaria', 19),
(197, 'Coxs Bazar Sadar', 19),
(198, 'Kutubdia', 19),
(199, 'Maheshkhali', 19),
(200, 'Pekua', 19),
(201, 'Ramu', 19),
(202, 'Teknaf', 19),
(203, 'Ukhia', 19);

-- Feni District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(204, 'Chhagalnaiya', 20),
(205, 'Daganbhuiyan', 20),
(206, 'Feni Sadar', 20),
(207, 'Fulgazi', 20),
(208, 'Parshuram', 20),
(209, 'Sonagazi', 20);

-- Khagrachari District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(210, 'Dighinala', 21),
(211, 'Khagrachari Sadar', 21),
(212, 'Lakshmichhari', 21),
(213, 'Mahalchhari', 21),
(214, 'Manikchhari', 21),
(215, 'Matiranga', 21),
(216, 'Panchhari', 21),
(217, 'Ramgarh', 21),
(218, 'Guimara', 21);

-- Lakshmipur District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(219, 'Lakshmipur Sadar', 22),
(220, 'Raipur', 22),
(221, 'Ramganj', 22),
(222, 'Ramgati', 22),
(223, 'Kamalnagar', 22);

-- Noakhali District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(224, 'Begumganj', 23),
(225, 'Chatkhil', 23),
(226, 'Companiganj', 23),
(227, 'Hatiya', 23),
(228, 'Kabirhat', 23),
(229, 'Noakhali Sadar', 23),
(230, 'Senbagh', 23),
(231, 'Sonaimuri', 23),
(232, 'Subarnachar', 23);

-- Rangamati District (10 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(233, 'Baghaichhari', 24),
(234, 'Barkal', 24),
(235, 'Kawkhali', 24),
(236, 'Belaichhari', 24),
(237, 'Kaptai', 24),
(238, 'Juraichhari', 24),
(239, 'Langadu', 24),
(240, 'Naniarchar', 24),
(241, 'Rajasthali', 24),
(242, 'Rangamati Sadar', 24);

-- Bogura District (12 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(243, 'Adamdighi', 25),
(244, 'Bogura Sadar', 25),
(245, 'Dhunat', 25),
(246, 'Dhupchanchia', 25),
(247, 'Gabtali', 25),
(248, 'Kahaloo', 25),
(249, 'Nandigram', 25),
(250, 'Sariakandi', 25),
(251, 'Shajahanpur', 25),
(252, 'Sherpur', 25),
(253, 'Shibganj', 25),
(254, 'Sonatala', 25);

-- Joypurhat District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(255, 'Akkelpur', 26),
(256, 'Joypurhat Sadar', 26),
(257, 'Kalai', 26),
(258, 'Khetlal', 26),
(259, 'Panchbibi', 26);

-- Naogaon District (11 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(260, 'Atrai', 27),
(261, 'Badalgachhi', 27),
(262, 'Dhamoirhat', 27),
(263, 'Manda', 27),
(264, 'Mohadevpur', 27),
(265, 'Naogaon Sadar', 27),
(266, 'Niamatpur', 27),
(267, 'Patnitala', 27),
(268, 'Porsha', 27),
(269, 'Raninagar', 27),
(270, 'Sapahar', 27);

-- Natore District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(271, 'Bagatipara', 28),
(272, 'Baraigram', 28),
(273, 'Gurudaspur', 28),
(274, 'Lalpur', 28),
(275, 'Naldanga', 28),
(276, 'Natore Sadar', 28),
(277, 'Singra', 28);

-- Chapainawabganj District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(278, 'Bholahat', 29),
(279, 'Gomastapur', 29),
(280, 'Nachole', 29),
(281, 'Chapainawabganj Sadar', 29),
(282, 'Shibganj', 29);

-- Pabna District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(283, 'Atgharia', 30),
(284, 'Bera', 30),
(285, 'Bhangura', 30),
(286, 'Chatmohar', 30),
(287, 'Faridpur', 30),
(288, 'Ishwardi', 30),
(289, 'Pabna Sadar', 30),
(290, 'Santhia', 30),
(291, 'Sujanagar', 30);

-- Rajshahi District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(292, 'Bagha', 31),
(293, 'Bagmara', 31),
(294, 'Charghat', 31),
(295, 'Durgapur', 31),
(296, 'Godagari', 31),
(297, 'Mohanpur', 31),
(298, 'Paba', 31),
(299, 'Puthia', 31),
(300, 'Tanore', 31);

-- Sirajganj District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(301, 'Belkuchi', 32),
(302, 'Chauhali', 32),
(303, 'Kamarkhanda', 32),
(304, 'Kazipur', 32),
(305, 'Raiganj', 32),
(306, 'Shahjadpur', 32),
(307, 'Sirajganj Sadar', 32),
(308, 'Tarash', 32),
(309, 'Ullahpara', 32);

-- Bagerhat District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(310, 'Bagerhat Sadar', 33),
(311, 'Chitalmari', 33),
(312, 'Fakirhat', 33),
(313, 'Kachua', 33),
(314, 'Mollahat', 33),
(315, 'Mongla', 33),
(316, 'Morrelganj', 33),
(317, 'Rampal', 33),
(318, 'Sarankhola', 33);

-- Chuadanga District (4 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(319, 'Alamdanga', 34),
(320, 'Chuadanga Sadar', 34),
(321, 'Damurhuda', 34),
(322, 'Jibannagar', 34);

-- Jessore District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(323, 'Abhaynagar', 35),
(324, 'Bagherpara', 35),
(325, 'Chaugachha', 35),
(326, 'Jhikargachha', 35),
(327, 'Keshabpur', 35),
(328, 'Jessore Sadar', 35),
(329, 'Manirampur', 35),
(330, 'Sharsha', 35);

-- Jhenaidah District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(331, 'Harinakunda', 36),
(332, 'Jhenaidah Sadar', 36),
(333, 'Kaliganj', 36),
(334, 'Kotchandpur', 36),
(335, 'Maheshpur', 36),
(336, 'Shailkupa', 36);

-- Khulna District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(337, 'Batiaghata', 37),
(338, 'Dacope', 37),
(339, 'Dumuria', 37),
(340, 'Dighalia', 37),
(341, 'Koyra', 37),
(342, 'Paikgachha', 37),
(343, 'Phultala', 37),
(344, 'Rupsa', 37),
(345, 'Terokhada', 37);

-- Kushtia District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(346, 'Bheramara', 38),
(347, 'Daulatpur', 38),
(348, 'Khoksa', 38),
(349, 'Kumarkhali', 38),
(350, 'Kushtia Sadar', 38),
(351, 'Mirpur', 38);

-- Magura District (4 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(352, 'Magura Sadar', 39),
(353, 'Mohammadpur', 39),
(354, 'Shalikha', 39),
(355, 'Sreepur', 39);

-- Meherpur District (3 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(356, 'Gangni', 40),
(357, 'Meherpur Sadar', 40),
(358, 'Mujibnagar', 40);

-- Narail District (3 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(359, 'Kalia', 41),
(360, 'Lohagara', 41),
(361, 'Narail Sadar', 41);

-- Satkhira District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(362, 'Assasuni', 42),
(363, 'Debhata', 42),
(364, 'Kalaroa', 42),
(365, 'Kaliganj', 42),
(366, 'Satkhira Sadar', 42),
(367, 'Shyamnagar', 42),
(368, 'Tala', 42);

-- Barguna District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(369, 'Amtali', 43),
(370, 'Bamna', 43),
(371, 'Barguna Sadar', 43),
(372, 'Betagi', 43),
(373, 'Patharghata', 43),
(374, 'Taltali', 43);

-- Barishal District (10 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(375, 'Agailjhara', 44),
(376, 'Babuganj', 44),
(377, 'Bakerganj', 44),
(378, 'Banaripara', 44),
(379, 'Barishal Sadar', 44),
(380, 'Gournadi', 44),
(381, 'Hizla', 44),
(382, 'Mehendiganj', 44),
(383, 'Muladi', 44),
(384, 'Wazirpur', 44);

-- Bhola District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(385, 'Bhola Sadar', 45),
(386, 'Burhanuddin', 45),
(387, 'Char Fasson', 45),
(388, 'Daulatkhan', 45),
(389, 'Lalmohan', 45),
(390, 'Manpura', 45),
(391, 'Tazumuddin', 45);

-- Jhalokati District (4 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(392, 'Jhalokati Sadar', 46),
(393, 'Kathalia', 46),
(394, 'Nalchity', 46),
(395, 'Rajapur', 46);

-- Patuakhali District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(396, 'Bauphal', 47),
(397, 'Dashmina', 47),
(398, 'Dumki', 47),
(399, 'Galachipa', 47),
(400, 'Kalapara', 47),
(401, 'Mirzaganj', 47),
(402, 'Patuakhali Sadar', 47),
(403, 'Rangabali', 47);

-- Pirojpur District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(404, 'Bhandaria', 48),
(405, 'Kawkhali', 48),
(406, 'Mathbaria', 48),
(407, 'Nazirpur', 48),
(408, 'Nesarabad', 48),
(409, 'Pirojpur Sadar', 48),
(410, 'Indurkani', 48);

-- Habiganj District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(411, 'Ajmiriganj', 49),
(412, 'Bahubal', 49),
(413, 'Baniyachong', 49),
(414, 'Chunarughat', 49),
(415, 'Habiganj Sadar', 49),
(416, 'Lakhai', 49),
(417, 'Madhabpur', 49),
(418, 'Nabiganj', 49);

-- Moulvibazar District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(419, 'Barlekha', 50),
(420, 'Juri', 50),
(421, 'Kamalganj', 50),
(422, 'Kulaura', 50),
(423, 'Moulvibazar Sadar', 50),
(424, 'Rajnagar', 50),
(425, 'Sreemangal', 50);

-- Sunamganj District (11 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(426, 'Bishwamvarpur', 51),
(427, 'Chhatak', 51),
(428, 'Derai', 51),
(429, 'Dharamapasha', 51),
(430, 'Dowarabazar', 51),
(431, 'Jagannathpur', 51),
(432, 'Jamalganj', 51),
(433, 'Sulla', 51),
(434, 'Sunamganj Sadar', 51),
(435, 'Tahirpur', 51),
(436, 'Shanthiganj', 51);

-- Sylhet District (13 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(437, 'Balaganj', 52),
(438, 'Beanibazar', 52),
(439, 'Bishwanath', 52),
(440, 'Companiganj', 52),
(441, 'Dakshin Surma', 52),
(442, 'Fenchuganj', 52),
(443, 'Golapganj', 52),
(444, 'Gowainghat', 52),
(445, 'Jaintiapur', 52),
(446, 'Kanaighat', 52),
(447, 'Osmani Nagar', 52),
(448, 'Sylhet Sadar', 52),
(449, 'Zakiganj', 52);

-- Dinajpur District (13 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(450, 'Birampur', 53),
(451, 'Birganj', 53),
(452, 'Biral', 53),
(453, 'Bochaganj', 53),
(454, 'Chirirbandar', 53),
(455, 'Dinajpur Sadar', 53),
(456, 'Ghoraghat', 53),
(457, 'Hakimpur', 53),
(458, 'Kaharole', 53),
(459, 'Khansama', 53),
(460, 'Nawabganj', 53),
(461, 'Parbatipur', 53),
(462, 'Phulbari', 53);

-- Gaibandha District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(463, 'Fulchhari', 54),
(464, 'Gaibandha Sadar', 54),
(465, 'Gobindaganj', 54),
(466, 'Palashbari', 54),
(467, 'Sadullapur', 54),
(468, 'Saghata', 54),
(469, 'Sundarganj', 54);

-- Kurigram District (9 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(470, 'Bhurungamari', 55),
(471, 'Char Rajibpur', 55),
(472, 'Chilmari', 55),
(473, 'Kurigram Sadar', 55),
(474, 'Nageshwari', 55),
(475, 'Phulbari', 55),
(476, 'Rajarhat', 55),
(477, 'Raumari', 55),
(478, 'Ulipur', 55);

-- Lalmonirhat District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(479, 'Aditmari', 56),
(480, 'Hatibandha', 56),
(481, 'Kaliganj', 56),
(482, 'Lalmonirhat Sadar', 56),
(483, 'Patgram', 56);

-- Nilphamari District (6 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(484, 'Dimla', 57),
(485, 'Domar', 57),
(486, 'Jaldhaka', 57),
(487, 'Kishoreganj', 57),
(488, 'Nilphamari Sadar', 57),
(489, 'Saidpur', 57);

-- Panchagarh District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(490, 'Atwari', 58),
(491, 'Boda', 58),
(492, 'Debiganj', 58),
(493, 'Panchagarh Sadar', 58),
(494, 'Tetulia', 58);

-- Rangpur District (8 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(495, 'Badarganj', 59),
(496, 'Gangachara', 59),
(497, 'Kaunia', 59),
(498, 'Mithapukur', 59),
(499, 'Pirgachha', 59),
(500, 'Pirganj', 59),
(501, 'Rangpur Sadar', 59),
(502, 'Taraganj', 59);

-- Thakurgaon District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(503, 'Baliadangi', 60),
(504, 'Haripur', 60),
(505, 'Pirganj', 60),
(506, 'Ranisankail', 60),
(507, 'Thakurgaon Sadar', 60);

-- Jamalpur District (7 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(508, 'Baksiganj', 61),
(509, 'Dewanganj', 61),
(510, 'Islampur', 61),
(511, 'Jamalpur Sadar', 61),
(512, 'Madarganj', 61),
(513, 'Melandaha', 61),
(514, 'Sarishabari', 61);

-- Mymensingh District (13 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(515, 'Bhaluka', 62),
(516, 'Dhobaura', 62),
(517, 'Fulbaria', 62),
(518, 'Gaffargaon', 62),
(519, 'Gauripur', 62),
(520, 'Haluaghat', 62),
(521, 'Ishwarganj', 62),
(522, 'Mymensingh Sadar', 62),
(523, 'Muktagachha', 62),
(524, 'Nandail', 62),
(525, 'Phulpur', 62),
(526, 'Trishal', 62),
(527, 'Tara Khanda', 62);

-- Netrokona District (10 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(528, 'Atpara', 63),
(529, 'Barhatta', 63),
(530, 'Durgapur', 63),
(531, 'Khaliajuri', 63),
(532, 'Kalmakanda', 63),
(533, 'Kendua', 63),
(534, 'Madan', 63),
(535, 'Mohanganj', 63),
(536, 'Netrokona Sadar', 63),
(537, 'Purbadhala', 63);

-- Sherpur District (5 upazilas)
INSERT INTO upazilas (upazila_id, upazila_name, district_id) VALUES
(538, 'Jhenaigati', 64),
(539, 'Nakla', 64),
(540, 'Nalitabari', 64),
(541, 'Sherpur Sadar', 64),
(542, 'Sreebardi', 64);

-- ============================================
-- SUMMARY
-- ============================================
-- Total Divisions: 8
-- Total Districts: 64
-- Total Upazilas: 492
-- ============================================

-- Symptoms
INSERT INTO symptoms (symptom_id, symptom_name, symptom_image) VALUES
(1, 'Fever', '/images/symptoms/fever.jpg'),
(2, 'Cough', '/images/symptoms/cough.jpg'),
(3, 'Headache', '/images/symptoms/headache.jpg'),
(4, 'Stomach Pain', '/images/symptoms/stomach_pain.jpg'),
(5, 'Back Pain', '/images/symptoms/back_pain.jpg'),
(6, 'Chest Pain', '/images/symptoms/chest_pain.jpg'),
(7, 'Skin Rash', '/images/symptoms/skin_rash.jpg'),
(8, 'Diabetes', '/images/symptoms/diabetes.jpg'),
(9, 'High Blood Pressure', '/images/symptoms/blood_pressure.jpg'),
(10, 'Asthma', '/images/symptoms/asthma.jpg'),
(11, 'Joint Pain', '/images/symptoms/joint_pain.jpg'),
(12, 'Depression', '/images/symptoms/depression.jpg');

-- Departments
INSERT INTO departments (department_id, department_name, department_image) VALUES
(1, 'General Medicine', '/images/departments/general_medicine.jpg'),
(2, 'Cardiology', '/images/departments/cardiology.jpg'),
(3, 'Pediatrics', '/images/departments/pediatrics.jpg'),
(4, 'Orthopedics', '/images/departments/orthopedics.jpg'),
(5, 'Dermatology', '/images/departments/dermatology.jpg'),
(6, 'Gastroenterology', '/images/departments/gastroenterology.jpg'),
(7, 'Neurology', '/images/departments/neurology.jpg'),
(8, 'Psychiatry', '/images/departments/psychiatry.jpg'),
(9, 'Gynecology', '/images/departments/gynecology.jpg'),
(10, 'ENT', '/images/departments/ent.jpg'),
(11, 'Ophthalmology', '/images/departments/ophthalmology.jpg'),
(12, 'Dental', '/images/departments/dental.jpg');

-- ------------------------------
-- Core User Tables
-- ------------------------------

-- Users (Patients: 1-15, Doctors: 16-25, Admins: 26-30)
INSERT INTO users (user_id, first_name, last_name, email, password_hash, phone, role_id, created_at, updated_at) VALUES
(1, 'Rafiq', 'Ahmed', 'rafiq.ahmed@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '01712345678', 1, NOW() - INTERVAL '6 months', NOW()),
(2, 'Fatima', 'Begum', 'fatima.begum@yahoo.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123457', '01812345679', 1, NOW() - INTERVAL '5 months', NOW()),
(3, 'Karim', 'Hossain', 'karim.hossain@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123458', '01912345680', 1, NOW() - INTERVAL '4 months', NOW()),
(4, 'Nasrin', 'Akter', 'nasrin.akter@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123459', '01612345681', 1, NOW() - INTERVAL '3 months', NOW()),
(5, 'Mehedi', 'Hasan', 'mehedi.hasan@outlook.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123460', '01712345682', 1, NOW() - INTERVAL '2 months', NOW()),
(6, 'Ayesha', 'Rahman', 'ayesha.rahman@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123461', '01812345683', 1, NOW() - INTERVAL '2 months', NOW()),
(7, 'Tanvir', 'Islam', 'tanvir.islam@yahoo.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123462', '01912345684', 1, NOW() - INTERVAL '1 month', NOW()),
(8, 'Sadia', 'Sultana', 'sadia.sultana@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123463', '01612345685', 1, NOW() - INTERVAL '1 month', NOW()),
(9, 'Amir', 'Khan', 'amir.khan@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123464', '01712345686', 1, NOW() - INTERVAL '20 days', NOW()),
(10, 'Ruma', 'Khatun', 'ruma.khatun@yahoo.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123465', '01812345687', 1, NOW() - INTERVAL '15 days', NOW()),
(11, 'Shakib', 'Mahmud', 'shakib.mahmud@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123466', '01912345688', 1, NOW() - INTERVAL '10 days', NOW()),
(12, 'Nadia', 'Chowdhury', 'nadia.chowdhury@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123467', '01612345689', 1, NOW() - INTERVAL '8 days', NOW()),
(13, 'Imran', 'Hossain', 'imran.hossain@outlook.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123468', '01712345690', 1, NOW() - INTERVAL '5 days', NOW()),
(14, 'Sharmin', 'Akhter', 'sharmin.akhter@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123469', '01812345691', 1, NOW() - INTERVAL '3 days', NOW()),
(15, 'Jamal', 'Uddin', 'jamal.uddin@yahoo.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123470', '01912345692', 1, NOW() - INTERVAL '1 day', NOW()),
-- Doctors
(16, 'Dr. Abdul', 'Karim', 'dr.abdul.karim@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123471', '01712345693', 2, NOW() - INTERVAL '3 years', NOW()),
(17, 'Dr. Sabina', 'Yasmin', 'dr.sabina.yasmin@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123472', '01812345694', 2, NOW() - INTERVAL '2 years', NOW()),
(18, 'Dr. Mahmudul', 'Haque', 'dr.mahmudul.haque@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123473', '01912345695', 2, NOW() - INTERVAL '2 years', NOW()),
(19, 'Dr. Farzana', 'Islam', 'dr.farzana.islam@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123474', '01612345696', 2, NOW() - INTERVAL '18 months', NOW()),
(20, 'Dr. Habibur', 'Rahman', 'dr.habibur.rahman@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123475', '01712345697', 2, NOW() - INTERVAL '1 year', NOW()),
(21, 'Dr. Tahmina', 'Begum', 'dr.tahmina.begum@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123476', '01812345698', 2, NOW() - INTERVAL '1 year', NOW()),
(22, 'Dr. Rashid', 'Ahmed', 'dr.rashid.ahmed@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123477', '01912345699', 2, NOW() - INTERVAL '10 months', NOW()),
(23, 'Dr. Sultana', 'Razia', 'dr.sultana.razia@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123478', '01612345700', 2, NOW() - INTERVAL '8 months', NOW()),
(24, 'Dr. Mizanur', 'Rahman', 'dr.mizanur.rahman@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123479', '01712345701', 2, NOW() - INTERVAL '6 months', NOW()),
(25, 'Dr. Nasima', 'Khatun', 'dr.nasima.khatun@hospital.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123480', '01812345702', 2, NOW() - INTERVAL '4 months', NOW()),
-- Admins
(26, 'Admin', 'Hossain', 'admin.hossain@healthsys.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123481', '01912345703', 3, NOW() - INTERVAL '5 years', NOW()),
(27, 'Supervisor', 'Rahman', 'supervisor.rahman@healthsys.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123482', '01612345704', 3, NOW() - INTERVAL '4 years', NOW()),
(28, 'Manager', 'Khan', 'manager.khan@healthsys.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123483', '01712345705', 4, NOW() - INTERVAL '3 years', NOW()),
(29, 'Support', 'Ahmed', 'support.ahmed@healthsys.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123484', '01812345706', 5, NOW() - INTERVAL '2 years', NOW()),
(30, 'Coordinator', 'Begum', 'coordinator.begum@healthsys.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123485', '01912345707', 3, NOW() - INTERVAL '1 year', NOW());

-- Patients
INSERT INTO patients (patient_id, date_of_birth, gender_id, division_id, district_id, upazila_id, exact_location, blood_group_id, medical_history) VALUES
(1, '1985-03-15', 1, 1, 1, 1, 'House 12, Road 5, Dhanmondi', 1, 'Hypertension since 2018'),
(2, '1990-07-22', 2, 1, 1, 2, 'Flat 4B, Gulshan Avenue', 3, 'No significant medical history'),
(3, '1978-11-30', 1, 1, 1, 3, 'Block D, Section 10, Mirpur', 5, 'Type 2 Diabetes, managed with medication'),
(4, '1995-05-18', 2, 1, 1, 4, 'House 45, Sector 7, Uttara', 2, 'Asthma - uses inhaler as needed'),
(5, '1982-09-25', 1, 1, 2, 5, 'Tongi, Gazipur Sadar', 1, 'Mild hypertension'),
(6, '1988-12-10', 2, 2, 3, 6, 'Patenga, Chattogram', 7, 'No known allergies'),
(7, '1992-04-08', 1, 2, 4, 7, 'Marine Drive, Teknaf', 3, 'Previous appendectomy in 2015'),
(8, '1987-08-14', 2, 3, 5, 8, 'Medical Road, Rajshahi Sadar', 5, 'Thyroid disorder - on levothyroxine'),
(9, '1980-01-20', 1, 4, 6, 9, 'KDA Avenue, Khulna Sadar', 1, 'High cholesterol'),
(10, '1993-06-05', 2, 6, 8, 10, 'Zindabazar, Sylhet Sadar', 3, 'Seasonal allergies'),
(11, '1975-10-12', 1, 7, 9, 11, 'Station Road, Rangpur Sadar', 5, 'Coronary artery disease, stent placed 2020'),
(12, '1991-02-28', 2, 8, 10, 12, 'Charpara, Mymensingh Sadar', 2, 'Migraine - occasional episodes'),
(13, '1986-07-16', 1, 1, 11, 1, 'Fatullah, Narayanganj', 1, 'Back pain - chronic'),
(14, '1994-03-22', 2, 2, 12, 3, 'Kandirpar, Comilla', 7, 'PCOS - under treatment'),
(15, '1983-11-09', 1, 1, 1, 2, 'Banani, Dhaka', 5, 'Gout - controlled with diet');

-- Doctors
INSERT INTO doctors (doctor_id, about, bmdc_number, qualification, total_experience, working_hours, profile_image, is_verified, division_id, district_id, upazila_id) VALUES
(16, 'Experienced cardiologist specializing in heart disease management and preventive cardiology.', 'A-45678', 'MBBS (DMC), MD (Cardiology)', 15, '{"monday": "9:00-17:00", "tuesday": "9:00-17:00", "wednesday": "9:00-17:00", "thursday": "9:00-17:00", "saturday": "9:00-13:00"}', '/images/doctors/dr_abdul_karim.jpg', true, 1, 1, 1),
(17, 'Pediatrician with expertise in child development and vaccination.', 'A-45679', 'MBBS (DMC), DCH, FCPS (Pediatrics)', 12, '{"monday": "10:00-16:00", "tuesday": "10:00-16:00", "wednesday": "10:00-16:00", "thursday": "10:00-16:00", "saturday": "10:00-14:00"}', '/images/doctors/dr_sabina_yasmin.jpg', true, 1, 1, 2),
(18, 'Orthopedic surgeon specializing in joint replacement and sports injuries.', 'A-45680', 'MBBS (CMC), MS (Orthopedics)', 10, '{"sunday": "9:00-17:00", "monday": "9:00-17:00", "tuesday": "9:00-17:00", "thursday": "9:00-17:00"}', '/images/doctors/dr_mahmudul_haque.jpg', true, 1, 1, 3),
(19, 'Dermatologist expert in treating skin disorders, acne, and cosmetic procedures.', 'A-45681', 'MBBS (DMC), DDV, MD (Dermatology)', 8, '{"monday": "14:00-20:00", "wednesday": "14:00-20:00", "thursday": "14:00-20:00", "saturday": "10:00-16:00"}', '/images/doctors/dr_farzana_islam.jpg', true, 1, 1, 4),
(20, 'General physician with focus on diabetes and hypertension management.', 'A-45682', 'MBBS (RMC), FCPS (Medicine)', 7, '{"sunday": "8:00-14:00", "monday": "8:00-14:00", "wednesday": "8:00-14:00", "friday": "8:00-14:00"}', '/images/doctors/dr_habibur_rahman.jpg', true, 1, 2, 5),
(21, 'Gynecologist specializing in pregnancy care and womens health issues.', 'A-45683', 'MBBS (SMC), FCPS (Gynecology)', 14, '{"sunday": "9:00-15:00", "tuesday": "9:00-15:00", "wednesday": "9:00-15:00", "thursday": "9:00-15:00"}', '/images/doctors/dr_tahmina_begum.jpg', true, 2, 3, 6),
(22, 'ENT specialist treating ear, nose, throat disorders and hearing problems.', 'A-45684', 'MBBS (CMC), FCPS (ENT)', 9, '{"monday": "15:00-21:00", "tuesday": "15:00-21:00", "thursday": "15:00-21:00", "saturday": "9:00-15:00"}', '/images/doctors/dr_rashid_ahmed.jpg', true, 2, 4, 7),
(23, 'Gastroenterologist expert in digestive system disorders and liver diseases.', 'A-45685', 'MBBS (DMC), MD (Gastroenterology)', 11, '{"sunday": "10:00-16:00", "monday": "10:00-16:00", "wednesday": "10:00-16:00", "thursday": "10:00-16:00"}', '/images/doctors/dr_sultana_razia.jpg', true, 3, 5, 8),
(24, 'Neurologist specializing in stroke, epilepsy, and neurological disorders.', 'A-45686', 'MBBS (DMC), MD (Neurology)', 6, '{"sunday": "9:00-17:00", "tuesday": "9:00-17:00", "wednesday": "9:00-17:00", "saturday": "9:00-13:00"}', '/images/doctors/dr_mizanur_rahman.jpg', true, 4, 6, 9),
(25, 'Psychiatrist providing mental health counseling and treatment.', 'A-45687', 'MBBS (SMC), MPhil (Psychiatry)', 5, '{"monday": "16:00-21:00", "tuesday": "16:00-21:00", "thursday": "16:00-21:00", "saturday": "10:00-16:00"}', '/images/doctors/dr_nasima_khatun.jpg', true, 6, 8, 10);

-- Doctor Experience
INSERT INTO doctor_experience (id, doctor_id, hospital_name, designation, department) VALUES
(1, 16, 'National Heart Foundation', 'Senior Consultant', 'Cardiology'),
(2, 16, 'United Hospital', 'Consultant', 'Cardiology'),
(3, 17, 'Dhaka Shishu Hospital', 'Senior Consultant', 'Pediatrics'),
(4, 18, 'Dhaka Medical College Hospital', 'Associate Professor', 'Orthopedics'),
(5, 19, 'Bangladesh Institute of Research & Rehabilitation', 'Consultant', 'Dermatology'),
(6, 20, 'Square Hospital', 'Consultant', 'General Medicine'),
(7, 21, 'Bangabandhu Sheikh Mujib Medical University', 'Assistant Professor', 'Gynecology'),
(8, 22, 'Chattogram Medical College Hospital', 'Associate Professor', 'ENT'),
(9, 23, 'Rajshahi Medical College Hospital', 'Senior Consultant', 'Gastroenterology'),
(10, 24, 'National Institute of Neurosciences', 'Consultant', 'Neurology'),
(11, 25, 'National Institute of Mental Health', 'Consultant', 'Psychiatry'),
(12, 16, 'Ibrahim Cardiac Hospital', 'Junior Consultant', 'Cardiology');

-- Doctor Specialization Departments
INSERT INTO doctor_specialization_departments (doctor_id, department_id) VALUES
(16, 2), -- Cardiology
(17, 3), -- Pediatrics
(18, 4), -- Orthopedics
(19, 5), -- Dermatology
(20, 1), -- General Medicine
(21, 9), -- Gynecology
(22, 10), -- ENT
(23, 6), -- Gastroenterology
(24, 7), -- Neurology
(25, 8), -- Psychiatry
(20, 2), -- General Medicine also knows Cardiology
(16, 1); -- Cardiologist also general medicine

-- Doctor Specialization Symptoms
INSERT INTO doctor_specialization_symptoms (doctor_id, symptom_id) VALUES
(16, 6), -- Chest Pain
(16, 9), -- High Blood Pressure
(17, 1), -- Fever
(17, 2), -- Cough
(18, 5), -- Back Pain
(18, 11), -- Joint Pain
(19, 7), -- Skin Rash
(20, 1), -- Fever
(20, 8), -- Diabetes
(20, 9), -- High Blood Pressure
(21, 4), -- Stomach Pain
(22, 2), -- Cough
(22, 3), -- Headache
(23, 4), -- Stomach Pain
(24, 3), -- Headache
(25, 12), -- Depression
(25, 3); -- Headache

-- Admins
INSERT INTO admins (admin_id, role_description) VALUES
(26, 'System Administrator - Full system access and management'),
(27, 'Supervisor - Monitors daily operations and staff performance'),
(28, 'Super Admin - Platform owner with highest privileges'),
(29, 'Support Staff - Handles user queries and technical support'),
(30, 'Operations Coordinator - Manages appointments and schedules');

-- ------------------------------
-- Appointment & Consultation
-- ------------------------------

-- Appointments
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status_id, reason, created_at, updated_at) VALUES
(1, 1, 16, '2024-10-28', '10:00:00', 2, 'Chest pain and shortness of breath', NOW() - INTERVAL '3 days', NOW()),
(2, 2, 17, '2024-10-29', '11:00:00', 2, 'Childs routine checkup and vaccination', NOW() - INTERVAL '2 days', NOW()),
(3, 3, 20, '2024-10-27', '09:00:00', 3, 'Diabetes follow-up consultation', NOW() - INTERVAL '5 days', NOW() - INTERVAL '1 day'),
(4, 4, 17, '2024-10-30', '14:00:00', 1, 'Asthma management', NOW() - INTERVAL '1 day', NOW()),
(5, 5, 16, '2024-10-26', '15:00:00', 3, 'Hypertension review', NOW() - INTERVAL '7 days', NOW() - INTERVAL '2 days'),
(6, 6, 23, '2024-11-01', '10:30:00', 1, 'Stomach issues and digestive problems', NOW(), NOW()),
(7, 7, 22, '2024-10-31', '16:00:00', 2, 'Throat infection and ear pain', NOW() - INTERVAL '1 day', NOW()),
(8, 8, 19, '2024-10-25', '14:30:00', 3, 'Skin rash treatment', NOW() - INTERVAL '10 days', NOW() - INTERVAL '5 days'),
(9, 9, 20, '2024-11-02', '08:30:00', 1, 'High cholesterol consultation', NOW(), NOW()),
(10, 10, 21, '2024-11-03', '09:30:00', 1, 'Pregnancy checkup', NOW(), NOW()),
(11, 11, 16, '2024-10-24', '11:00:00', 3, 'Heart disease follow-up', NOW() - INTERVAL '12 days', NOW() - INTERVAL '6 days'),
(12, 12, 24, '2024-11-04', '10:00:00', 2, 'Migraine consultation', NOW(), NOW()),
(13, 13, 18, '2024-10-28', '13:00:00', 2, 'Chronic back pain treatment', NOW() - INTERVAL '3 days', NOW()),
(14, 14, 21, '2024-10-29', '15:00:00', 4, 'PCOS treatment consultation', NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'),
(15, 15, 20, '2024-11-05', '12:00:00', 1, 'Gout management', NOW(), NOW());

-- Reminders
INSERT INTO reminders (reminder_id, appointment_id, user_id, reminder_type_id, message, sent_at, reminder_status_id) VALUES
(1, 1, 1, 1, 'Reminder: Your appointment with Dr. Abdul Karim is tomorrow at 10:00 AM', NOW() - INTERVAL '1 day', 2),
(2, 2, 2, 3, 'Appointment confirmation: Dr. Sabina Yasmin on Oct 29 at 11:00 AM', NOW() - INTERVAL '2 days', 3),
(3, 3, 3, 1, 'Your diabetes checkup with Dr. Habibur Rahman is scheduled', NOW() - INTERVAL '5 days', 2),
(4, 4, 4, 2, 'Reminder: Asthma consultation tomorrow at 2:00 PM with Dr. Sabina Yasmin', NOW() - INTERVAL '1 day', 2),
(5, 6, 6, 4, 'Upcoming appointment: Dr. Sultana Razia on Nov 1 at 10:30 AM', NOW() - INTERVAL '6 hours', 2),
(6, 7, 7, 1, 'Your ENT appointment with Dr. Rashid Ahmed is confirmed for Oct 31', NOW() - INTERVAL '2 days', 2),
(7, 10, 10, 3, 'Pregnancy checkup reminder: Nov 3 at 9:30 AM with Dr. Tahmina Begum', NOW() - INTERVAL '12 hours', 2),
(8, 12, 12, 1, 'Appointment with Dr. Mizanur Rahman tomorrow at 10:00 AM', NOW() - INTERVAL '1 day', 2),
(9, 13, 13, 2, 'Back pain consultation confirmed with Dr. Mahmudul Haque', NOW() - INTERVAL '3 days', 3),
(10, 15, 15, 1, 'Gout management appointment on Nov 5 at 12:00 PM', NOW() - INTERVAL '1 day', 1),
(11, 1, 16, 6, 'New patient appointment: Rafiq Ahmed on Oct 28 at 10:00 AM', NOW() - INTERVAL '3 days', 3),
(12, 9, 9, 1, 'Appointment reminder: Nov 2 at 8:30 AM with Dr. Habibur Rahman', NOW() - INTERVAL '18 hours', 2);

-- Prescriptions
INSERT INTO prescriptions (prescription_id, appointment_id, doctor_id, patient_id, prescription_text, issued_at) VALUES
(1, 3, 20, 3, 'Rx: Tab. Metformin 500mg - 1+0+1 after meals for 30 days. Tab. Glimepiride 2mg - 1+0+0 before breakfast. Blood sugar monitoring recommended. Follow-up after 1 month.', NOW() - INTERVAL '1 day'),
(2, 5, 16, 5, 'Rx: Tab. Amlodipine 5mg - 0+0+1 daily. Tab. Atorvastatin 20mg - 0+0+1 after dinner. Reduce salt intake. Regular BP monitoring. Next visit after 2 months.', NOW() - INTERVAL '2 days'),
(3, 8, 19, 8, 'Rx: Cream Hydrocortisone 1% - Apply twice daily on affected area. Tab. Cetirizine 10mg - 0+0+1 at night for 7 days. Avoid direct sunlight. Follow-up if no improvement.', NOW() - INTERVAL '5 days'),
(4, 11, 16, 11, 'Rx: Tab. Clopidogrel 75mg - 1+0+0 after breakfast. Tab. Rosuvastatin 10mg - 0+0+1 after dinner. Continue previous cardiac medications. Regular exercise advised. Next checkup in 3 months.', NOW() - INTERVAL '6 days'),
(5, 3, 20, 3, 'Rx: Continue Metformin 500mg. Added Tab. Vitamin B12 - 1+0+0 daily. Dietary advice: reduce carbohydrates, increase vegetables. HbA1c test recommended after 3 months.', NOW() - INTERVAL '1 day'),
(6, 5, 16, 5, 'Rx: Increased Amlodipine to 10mg - 0+0+1 daily due to uncontrolled BP. Continue Atorvastatin. Low sodium diet strictly. Walking 30 min daily recommended.', NOW() - INTERVAL '2 days'),
(7, 8, 19, 8, 'Rx: Tab. Fexofenadine 120mg - 1+0+0 for 10 days. Cream Mometasone 0.1% - Apply once daily. Avoid wool clothing. Allergy test suggested.', NOW() - INTERVAL '5 days'),
(8, 11, 16, 11, 'Rx: Tab. Aspirin 75mg - 1+0+0 after breakfast. Tab. Ramipril 5mg - 1+0+0. ECG and Echo recommended. Stress management important. 6-month review scheduled.', NOW() - INTERVAL '6 days'),
(9, 1, 16, 1, 'Rx: Tab. Telmisartan 40mg - 1+0+0 morning. Tab. Propranolol 40mg - 0+1+0. ECG shows mild irregularity. Echocardiogram scheduled. Reduce smoking immediately.', NOW() - INTERVAL '3 days'),
(10, 7, 22, 7, 'Rx: Cap. Amoxicillin 500mg - 1+1+1 for 7 days. Syrup Chlorpheniramine - 2 tsf thrice daily. Gargle with warm salt water. Avoid cold drinks. Review after 1 week.', NOW() - INTERVAL '1 day');

-- Doctor Reviews
INSERT INTO doctor_reviews (review_id, doctor_id, patient_id, rating, review_text, created_at) VALUES
(1, 16, 1, 5, 'Excellent doctor! Very thorough examination and explained everything clearly. Highly recommended for heart problems.', NOW() - INTERVAL '2 days'),
(2, 17, 2, 5, 'Dr. Sabina is wonderful with children. My son was comfortable throughout the checkup. Very professional and caring.', NOW() - INTERVAL '1 day'),
(3, 20, 3, 4, 'Good doctor, listens to patient concerns. Waiting time was a bit long but consultation was worth it.', NOW() - INTERVAL '1 day'),
(4, 19, 8, 5, 'Very satisfied with the treatment. My skin condition improved significantly. Will definitely visit again.', NOW() - INTERVAL '4 days'),
(5, 16, 5, 5, 'Dr. Abdul Karim saved my life. His expertise in cardiology is exceptional. Forever grateful.', NOW() - INTERVAL '2 days'),
(6, 16, 11, 5, 'Best cardiologist in Dhaka. Very experienced and genuinely cares about patients wellbeing.', NOW() - INTERVAL '5 days'),
(7, 22, 7, 4, 'Effective treatment for my throat infection. Doctor was professional but appointment was slightly delayed.', NOW() - INTERVAL '6 hours'),
(8, 20, 3, 5, 'Managing my diabetes excellently. Always available for queries. Highly recommended for diabetic patients.', NOW() - INTERVAL '12 hours'),
(9, 17, 4, 5, 'Great pediatrician! My daughter feels safe with her. Explains everything to both parent and child.', NOW() - INTERVAL '3 hours'),
(10, 19, 8, 4, 'Good dermatologist. Treatment is working well. Would give 5 stars if appointment scheduling was easier.', NOW() - INTERVAL '3 days'),
(11, 18, 13, 5, 'Excellent orthopedic surgeon. My back pain has reduced significantly after his treatment.', NOW() - INTERVAL '1 day'),
(12, 23, 6, 4, 'Knowledgeable gastroenterologist. Helped identify my digestive issues. Waiting for full recovery.', NOW() - INTERVAL '2 hours');

-- ------------------------------
-- Payments
-- ------------------------------

-- Payments
INSERT INTO payments (payment_id, appointment_id, patient_id, doctor_id, amount, method_id, status_id, transaction_time) VALUES
(1, 3, 3, 20, 1200.00, 1, 2, NOW() - INTERVAL '5 days'),
(2, 5, 5, 16, 1500.00, 2, 2, NOW() - INTERVAL '7 days'),
(3, 8, 8, 19, 1000.00, 1, 2, NOW() - INTERVAL '10 days'),
(4, 11, 11, 16, 1500.00, 4, 2, NOW() - INTERVAL '12 days'),
(5, 1, 1, 16, 1500.00, 1, 2, NOW() - INTERVAL '3 days'),
(6, 2, 2, 17, 1200.00, 3, 2, NOW() - INTERVAL '2 days'),
(7, 7, 7, 22, 1100.00, 1, 2, NOW() - INTERVAL '1 day'),
(8, 4, 4, 17, 1200.00, 2, 1, NOW() - INTERVAL '1 day'),
(9, 6, 6, 23, 1300.00, 1, 1, NOW() - INTERVAL '6 hours'),
(10, 9, 9, 20, 1200.00, 2, 1, NOW() - INTERVAL '3 hours'),
(11, 10, 10, 21, 1400.00, 1, 1, NOW() - INTERVAL '2 hours'),
(12, 12, 12, 24, 1600.00, 3, 1, NOW() - INTERVAL '1 hour'),
(13, 13, 13, 18, 1500.00, 1, 2, NOW() - INTERVAL '3 days'),
(14, 14, 14, 21, 1400.00, 2, 5, NOW() - INTERVAL '2 days'),
(15, 15, 15, 20, 1200.00, 1, 1, NOW() - INTERVAL '30 minutes');

-- Commissions
INSERT INTO commissions (commission_id, payment_id, admin_id, commission_amount, created_at) VALUES
(1, 1, 26, 180.00, NOW() - INTERVAL '5 days'),
(2, 2, 26, 225.00, NOW() - INTERVAL '7 days'),
(3, 3, 27, 150.00, NOW() - INTERVAL '10 days'),
(4, 4, 26, 225.00, NOW() - INTERVAL '12 days'),
(5, 5, 26, 225.00, NOW() - INTERVAL '3 days'),
(6, 6, 27, 180.00, NOW() - INTERVAL '2 days'),
(7, 7, 26, 165.00, NOW() - INTERVAL '1 day'),
(8, 13, 27, 225.00, NOW() - INTERVAL '3 days'),
(9, 1, 28, 120.00, NOW() - INTERVAL '5 days'),
(10, 2, 28, 150.00, NOW() - INTERVAL '7 days');

-- ------------------------------
-- Chat & Security
-- ------------------------------

-- Chat Messages
INSERT INTO chat_messages (message_id, appointment_id, sender_id, receiver_id, message_text, sent_at) VALUES
(1, 1, 1, 16, 'Good morning Doctor, I have been experiencing chest pain for the last 2 days.', NOW() - INTERVAL '4 days'),
(2, 1, 16, 1, 'Good morning. Can you describe the pain? Is it sharp or dull? Does it radiate to your arm?', NOW() - INTERVAL '4 days' + INTERVAL '5 minutes'),
(3, 1, 1, 16, 'It is a dull pain, mostly in the center of my chest. Sometimes I feel shortness of breath.', NOW() - INTERVAL '4 days' + INTERVAL '10 minutes'),
(4, 1, 16, 1, 'I see. This needs immediate attention. Please come to the hospital today. I have scheduled your appointment.', NOW() - INTERVAL '4 days' + INTERVAL '15 minutes'),
(5, 2, 2, 17, 'Doctor, is my sons vaccination up to date?', NOW() - INTERVAL '3 days'),
(6, 2, 17, 2, 'Let me check his records. Yes, he is due for his MMR vaccine. Please bring his vaccination card.', NOW() - INTERVAL '3 days' + INTERVAL '20 minutes'),
(7, 3, 3, 20, 'My sugar level was 180 this morning. Should I be concerned?', NOW() - INTERVAL '6 days'),
(8, 3, 20, 3, 'That is slightly elevated. Are you taking your medication regularly? Please maintain a food diary.', NOW() - INTERVAL '6 days' + INTERVAL '30 minutes'),
(9, 7, 7, 22, 'Doctor, my throat pain has worsened. Can I get an earlier appointment?', NOW() - INTERVAL '2 days'),
(10, 7, 22, 7, 'I understand. Please come tomorrow at 4 PM. Meanwhile, gargle with warm salt water 3-4 times daily.', NOW() - INTERVAL '2 days' + INTERVAL '1 hour'),
(11, 10, 10, 21, 'This is my first pregnancy. I am a bit nervous about the checkup.', NOW() - INTERVAL '1 day'),
(12, 10, 21, 10, 'Do not worry at all. It is completely normal to feel this way. We will go through everything step by step.', NOW() - INTERVAL '1 day' + INTERVAL '15 minutes'),
(13, 13, 13, 18, 'My back pain is unbearable at night. What can I do for relief?', NOW() - INTERVAL '4 days'),
(14, 13, 18, 13, 'Try applying hot compress before sleep. Avoid sleeping on soft mattress. We will discuss treatment options during appointment.', NOW() - INTERVAL '4 days' + INTERVAL '45 minutes'),
(15, 6, 6, 23, 'I have been having stomach issues for a week. Should I fast before the appointment?', NOW() - INTERVAL '1 day'),
(16, 6, 23, 6, 'Yes, please fast for 8 hours before the appointment. You can drink water. This will help with proper examination.', NOW() - INTERVAL '1 day' + INTERVAL '2 hours');

-- Call Sessions
INSERT INTO call_sessions (call_id, appointment_id, doctor_id, patient_id, call_type, started_at, ended_at, duration) VALUES
(1, 3, 20, 3, 'video', NOW() - INTERVAL '5 days' + INTERVAL '9 hours', NOW() - INTERVAL '5 days' + INTERVAL '9 hours 15 minutes', '00:15:00'),
(2, 5, 16, 5, 'video', NOW() - INTERVAL '7 days' + INTERVAL '15 hours', NOW() - INTERVAL '7 days' + INTERVAL '15 hours 20 minutes', '00:20:00'),
(3, 8, 19, 8, 'video', NOW() - INTERVAL '10 days' + INTERVAL '14 hours 30 minutes', NOW() - INTERVAL '10 days' + INTERVAL '14 hours 45 minutes', '00:15:00'),
(4, 11, 16, 11, 'video', NOW() - INTERVAL '12 days' + INTERVAL '11 hours', NOW() - INTERVAL '12 days' + INTERVAL '11 hours 25 minutes', '00:25:00'),
(5, 1, 16, 1, 'video', NOW() - INTERVAL '3 days' + INTERVAL '10 hours', NOW() - INTERVAL '3 days' + INTERVAL '10 hours 18 minutes', '00:18:00'),
(6, 7, 22, 7, 'audio', NOW() - INTERVAL '1 day' + INTERVAL '16 hours', NOW() - INTERVAL '1 day' + INTERVAL '16 hours 12 minutes', '00:12:00'),
(7, 13, 18, 13, 'video', NOW() - INTERVAL '3 days' + INTERVAL '13 hours', NOW() - INTERVAL '3 days' + INTERVAL '13 hours 22 minutes', '00:22:00'),
(8, 2, 17, 2, 'video', NOW() - INTERVAL '2 days' + INTERVAL '11 hours', NOW() - INTERVAL '2 days' + INTERVAL '11 hours 17 minutes', '00:17:00'),
(9, 6, 23, 6, 'audio', NOW() - INTERVAL '8 hours', NOW() - INTERVAL '8 hours' + INTERVAL '10 minutes', '00:10:00'),
(10, 10, 21, 10, 'video', NOW() - INTERVAL '4 hours', NOW() - INTERVAL '4 hours' + INTERVAL '20 minutes', '00:20:00');

-- Audit Logs
INSERT INTO audit_logs (log_id, user_id, action, table_name, record_id, timestamp, details) VALUES
(1, 1, 'CREATE', 'appointments', 1, NOW() - INTERVAL '3 days', '{"action": "Patient created new appointment", "doctor": "Dr. Abdul Karim"}'),
(2, 16, 'UPDATE', 'appointments', 1, NOW() - INTERVAL '3 days', '{"action": "Doctor confirmed appointment", "status": "confirmed"}'),
(3, 3, 'CREATE', 'appointments', 3, NOW() - INTERVAL '5 days', '{"action": "Patient booked follow-up appointment"}'),
(4, 20, 'CREATE', 'prescriptions', 1, NOW() - INTERVAL '1 day', '{"action": "Doctor issued prescription", "patient": "Karim Hossain"}'),
(5, 26, 'UPDATE', 'doctors', 16, NOW() - INTERVAL '30 days', '{"action": "Admin verified doctor profile", "doctor": "Dr. Abdul Karim"}'),
(6, 8, 'CREATE', 'doctor_reviews', 4, NOW() - INTERVAL '4 days', '{"action": "Patient submitted review", "rating": 5}'),
(7, 1, 'UPDATE', 'payments', 5, NOW() - INTERVAL '3 days', '{"action": "Payment completed", "method": "bKash", "amount": 1500}'),
(8, 26, 'CREATE', 'commissions', 5, NOW() - INTERVAL '3 days', '{"action": "Commission calculated", "amount": 225}'),
(9, 7, 'CREATE', 'chat_messages', 9, NOW() - INTERVAL '2 days', '{"action": "Patient sent message to doctor"}'),
(10, 22, 'CREATE', 'chat_messages', 10, NOW() - INTERVAL '2 days', '{"action": "Doctor replied to patient message"}'),
(11, 16, 'CREATE', 'call_sessions', 5, NOW() - INTERVAL '3 days', '{"action": "Video consultation started", "duration": "18 minutes"}'),
(12, 2, 'UPDATE', 'users', 2, NOW() - INTERVAL '10 days', '{"action": "User updated profile information"}'),
(13, 28, 'DELETE', 'appointments', 14, NOW() - INTERVAL '1 day', '{"action": "Admin cancelled appointment", "reason": "Patient request"}'),
(14, 13, 'CREATE', 'appointments', 13, NOW() - INTERVAL '3 days', '{"action": "New appointment created", "department": "Orthopedics"}'),
(15, 18, 'UPDATE', 'appointments', 13, NOW() - INTERVAL '3 days', '{"action": "Doctor accepted appointment request"}');

-- Reset sequences to continue from current max values
SELECT setval('roles_role_id_seq', (SELECT MAX(role_id) FROM roles));
SELECT setval('genders_gender_id_seq', (SELECT MAX(gender_id) FROM genders));
SELECT setval('appointment_status_status_id_seq', (SELECT MAX(status_id) FROM appointment_status));
SELECT setval('reminder_types_reminder_type_id_seq', (SELECT MAX(reminder_type_id) FROM reminder_types));
SELECT setval('reminder_status_reminder_status_id_seq', (SELECT MAX(reminder_status_id) FROM reminder_status));
SELECT setval('payment_methods_method_id_seq', (SELECT MAX(method_id) FROM payment_methods));
SELECT setval('payment_status_status_id_seq', (SELECT MAX(status_id) FROM payment_status));
SELECT setval('blood_group_blood_group_id_seq', (SELECT MAX(blood_group_id) FROM blood_group));
SELECT setval('divisions_division_id_seq', (SELECT MAX(division_id) FROM divisions));
SELECT setval('districts_district_id_seq', (SELECT MAX(district_id) FROM districts));
SELECT setval('upazilas_upazila_id_seq', (SELECT MAX(upazila_id) FROM upazilas));
SELECT setval('symptoms_symptom_id_seq', (SELECT MAX(symptom_id) FROM symptoms));
SELECT setval('departments_department_id_seq', (SELECT MAX(department_id) FROM departments));
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('doctor_experience_id_seq', (SELECT MAX(id) FROM doctor_experience));
SELECT setval('appointments_appointment_id_seq', (SELECT MAX(appointment_id) FROM appointments));
SELECT setval('reminders_reminder_id_seq', (SELECT MAX(reminder_id) FROM reminders));
SELECT setval('prescriptions_prescription_id_seq', (SELECT MAX(prescription_id) FROM prescriptions));
SELECT setval('doctor_reviews_review_id_seq', (SELECT MAX(review_id) FROM doctor_reviews));
SELECT setval('payments_payment_id_seq', (SELECT MAX(payment_id) FROM payments));
SELECT setval('commissions_commission_id_seq', (SELECT MAX(commission_id) FROM commissions));
SELECT setval('chat_messages_message_id_seq', (SELECT MAX(message_id) FROM chat_messages));
SELECT setval('call_sessions_call_id_seq', (SELECT MAX(call_id) FROM call_sessions));
SELECT setval('audit_logs_log_id_seq', (SELECT MAX(log_id) FROM audit_logs));

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check record counts
SELECT 'roles' as table_name, COUNT(*) as record_count FROM roles
UNION ALL SELECT 'genders', COUNT(*) FROM genders
UNION ALL SELECT 'appointment_status', COUNT(*) FROM appointment_status
UNION ALL SELECT 'divisions', COUNT(*) FROM divisions
UNION ALL SELECT 'districts', COUNT(*) FROM districts
UNION ALL SELECT 'upazilas', COUNT(*) FROM upazilas
UNION ALL SELECT 'symptoms', COUNT(*) FROM symptoms
UNION ALL SELECT 'departments', COUNT(*) FROM departments
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'patients', COUNT(*) FROM patients
UNION ALL SELECT 'doctors', COUNT(*) FROM doctors
UNION ALL SELECT 'admins', COUNT(*) FROM admins
UNION ALL SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL SELECT 'prescriptions', COUNT(*) FROM prescriptions
UNION ALL SELECT 'doctor_reviews', COUNT(*) FROM doctor_reviews
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'chat_messages', COUNT(*) FROM chat_messages
UNION ALL SELECT 'call_sessions', COUNT(*) FROM call_sessions
UNION ALL SELECT 'audit_logs', COUNT(*) FROM audit_logs
ORDER BY table_name;