import LoginForm from '@/components/auth/LoginForm'
import Image from 'next/image'

export const metadata = {
  title: 'Login | Your App Name',
  description: 'Secure login to your account'
}

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="w-full max-w-md px-6">
        <div className="text-right mb-8">
          <Image 
            src="/logo.svg" 
            alt="Company Logo" 
            width={32}
            height={32}
            className="inline-block h-8"
          />
        </div>
        <LoginForm />
      </div>
    </main>
  )
}
