import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Add paths that don't require authentication
const publicPaths = ['/', '/login', '/api/auth/login']

export function middleware(request: NextRequest) {
  const currentUser = request.cookies.get('currentUser')?.value
  const path = request.nextUrl.pathname

  // Allow access to public paths and API routes
  if (publicPaths.includes(path) || path.startsWith('/api/')) {
    return NextResponse.next()
  }

  // Redirect to login if not authenticated
  if (!currentUser) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  try {
    const user = JSON.parse(currentUser)

    // Check role-based access
    if (path.startsWith('/dashboard') && user.role !== 'admin') {
      return NextResponse.redirect(new URL('/user-panel', request.url))
    }

    if (path.startsWith('/user-panel') && user.role === 'admin') {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }

    return NextResponse.next()
  } catch (error) {
    // If there's any error parsing the user data, redirect to login
    return NextResponse.redirect(new URL('/', request.url))
  }
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
} 