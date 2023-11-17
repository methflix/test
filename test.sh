#!/bin/bash

# Set the keyboard layout
loadkeys us

# Verify the boot mode (UEFI or BIOS)
if [ -d "/sys/firmware/efi/efivars" ]; then
    echo "UEFI mode detected."
else
    echo "BIOS mode detected. This script assumes UEFI mode, please modify accordingly."
    exit 1
fi

# Verify internet connectivity
ping -c 3 google.com || (echo "Please check your internet connection." && exit 1)

# Update the system clock
timedatectl set-ntp true

# Partition the disk (example assumes a simple layout, adjust as needed)
# This example uses parted for partitioning, but you can use other tools like fdisk, gdisk, etc.
echo "Partitioning the disk:"
echo "1. Create a partition for the root filesystem (choose ext4 or btrfs)"
select fs_type in "ext4" "btrfs"; do
    case $fs_type in
        ext4)
            mkfs.ext4 /dev/sda1
            root_fs="ext4"
            break
            ;;
        btrfs)
            mkfs.btrfs /dev/sda1
            root_fs="btrfs"
            break
            ;;
        *)
            echo "Invalid option. Please select 1 or 2."
            ;;
    esac
done

# Mount the root partition
mount /dev/sda1 /mnt

# Install the base system
pacstrap /mnt base linux linux-firmware

# Generate an fstab file
genfstab -U /mnt >> /mnt/etc/fstab

# Change root into the new system
arch-chroot /mnt

# Set the time zone
ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
hwclock --systohc

# Uncomment the desired locale(s) in /etc/locale.gen and generate them with:
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Set the hostname
echo "yourhostname" > /etc/hostname

# Set up networking
# (You may need to install additional network-related packages and configure them)

# Set up sudo privileges for a new user (replace 'username' with your desired username)
useradd -m -G wheel username
passwd username
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers

# Create and mount the home subvolume if using btrfs
if [ "$root_fs" = "btrfs" ]; then
    btrfs subvolume create /mnt/home
    umount /mnt
    mount -o subvol=home /dev/sda1 /mnt
fi

# Install and configure a bootloader (example uses GRUB for UEFI, adjust as needed)
pacman -S grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# Exit the chroot environment
exit

# Unmount all partitions
umount -R /mnt

# Reboot the system
reboot
